import os
import glob
import json
big_superb_path = "/mnt/data/big-superb-train-data-renamed"
train_prompt_path = "/home/stan/espnet/egs2/stop/big_superb/dump/raw/train/prompt"
train_prompt = open(train_prompt_path, 'r').readlines()
test_prompt_path = "/home/stan/espnet/egs2/stop/big_superb/dump/raw/test/prompt"
test_prompt = open(test_prompt_path, 'r').readlines()
test_unseen_path = "/home/stan/espnet/egs2/stop/big_superb/dump/raw/test/unseen"
test_unseen = open(test_unseen_path, 'w')
Seen_prompt = set()
for line in train_prompt:
    prompt = line.split("<|startofprev|>")[-1].split("The answer")[0].strip()
    Seen_prompt.add(prompt.strip())

# print(Seen_prompt)
seen = 0
for line in test_prompt:
    file = line.split("<|startofprev|>")[0].strip()
    prompt = line.split("<|startofprev|>")[-1].split("The answer")[0].strip()
    utt_id = line.split(" ", maxsplit=1)[0]
    if prompt in Seen_prompt:
        test_unseen.write(f"{utt_id} 0\n")
        seen += 1
    else:
        test_unseen.write(f"{utt_id} 1\n")
        
print(f"Seen {seen}/{len(test_prompt)} instructions")
    