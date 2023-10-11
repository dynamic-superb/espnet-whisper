#!/usr/bin/env bash

# Copyright 2021  Siddhant Arora
#           2021  Carnegie Mellon University
# Apache 2.0


import os
import re
import sys
import glob
import json
from tqdm import tqdm
if len(sys.argv) != 2:
    print("Usage: python data_prep.py [stop_root]")
    sys.exit(1)

def in_test_tasks(task):
    test_tasks = ["DialogueActPairing_DailyTalk_Test", "MultiSpeakerDetection_LibriSpeechTestClean","MultiSpeakerDetection_VCTK"]
    for test_task in test_tasks:
        if test_task in task:
            return True
    return False
stop_root = sys.argv[1]
split_dict = {
    "train": "train",
    "valid": "validation",
    "test": "test",
}

for x in split_dict.keys():
    with open(os.path.join("data", x, "text"), "w") as text_f, open(
        os.path.join("data", x, "wav.scp"), "w"
    ) as wav_scp_f, open(
        os.path.join("data", x, "transcript"), "w"
    ) as transcript_f, open(
        os.path.join("data", x, "utt2spk"), "w"
    ) as utt2spk_f, open(
        os.path.join("data", x, "filter_file"), "w"
    ) as filter_f:

        text_f.truncate()
        wav_scp_f.truncate()
        utt2spk_f.truncate()
        metadata_files = glob.glob(os.path.join(stop_root, "*", split_dict[x], "metadata.json"))
        # metadata_files = [file for file in metadata_files if in_test_tasks(file)]
        utt_id_set = set()
        # lines = sorted(transcript_df.values, key=lambda s: s[0])
        for metadata_file in tqdm(metadata_files, desc="All metafiles"):
            
            metadata = json.load(open(metadata_file, 'r'))
            sub_root = metadata_file.replace('metadata.json','')
            for file, info in tqdm(metadata.items()):
                utt_id = file
                if utt_id in utt_id_set:
                    filter_f.write(sub_root + file + "\n")
                    continue
                utt_id_set.add(utt_id)
                try:
                    words = str(info['label'])
                except:
                    print(file)
                    print(info)
                    raise NotImplementedError
                # print(utt_id + " " + words + "\n")
                text_f.write(utt_id + " " + words + "\n")
                wav_scp_f.write(utt_id + " " + sub_root + file + "\n")
                utt2spk_f.write(utt_id + " "+utt_id+" \n")
