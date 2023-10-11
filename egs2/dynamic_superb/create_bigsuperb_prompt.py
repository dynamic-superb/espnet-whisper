import json
from os.path import join
from tqdm import tqdm
import os
def parse_label(label_str):
    label_str = label_str.split('The answer could be ')[-1]
    [label1, label2] = label_str.replace('.', '').split(' or ')
    if ',' in label1:
        label1 = label1.split(',')
    else:
        label1 = [label1]
    return [l.strip() for l in label1 if l != ' '] + [label2.strip()] 
for split in ["train","valid", "test"]:
# for split in ["test_new"]:
    os.makedirs("dump/raw/"+split, exist_ok=True)
    data_table = open(f"data/{split}/wav.scp", 'r').readlines()
    data_table = {l.split()[0]:l.split()[1] for l in data_table}
    data=open("dump/raw/"+split+"/wav.scp", "r")
    file1=open("dump/raw/"+split+"/prompt", "w")
    file_emptytext=open("dump/raw/"+split+"/emptytext", "w")
    file1_new=open("dump/raw/"+split+"/prompt_new","w")
    file1_label=open("dump/raw/"+split+"/label","w")
    data = data.readlines()
    cur_subset = ""
    all_labels, utt_ids = {}, []
    for line in tqdm(data):
        utt_id, _ = line.split()[0], line.split()[1]
        utt_ids.append(utt_id)
        path = data_table[utt_id]
        subset = "/".join(path.split('/')[:-1])
        if subset not in all_labels:
            all_labels[subset] = {'utt_id':[], 'label':set()}
        if cur_subset != subset:
            # print("Reading ", subset)
            cur_subset = subset
            meta_data = json.load(open(join(subset, "metadata.json"), 'r'))
        
        all_labels[subset]['utt_id'].append(utt_id)
        all_labels[subset]['label'].add(str(meta_data[utt_id.split('/')[-1]]["label"]).strip())
        
        instruction = meta_data[utt_id.split('/')[-1]]["instruction"]
        prompt= "<|startofprev|> " + instruction
        if 'SpeechTextMatching' in subset or "SpokenTermDetection" in subset:
            text = meta_data[utt_id.split('/')[-1]]['text']
            prompt = f"<|text|> {text} {prompt}"
        file1.write(utt_id+" "+prompt+"\n")
        file1_new.write(utt_id+" "+prompt+"\n")
        
        file_emptytext.write(utt_id+" '' \n")
    
    id2label = {}
    for key, data in all_labels.items():
        for id in data['utt_id']:
            id2label[id] = ",".join(list(data['label']))
    for id in utt_ids:
        file1_label.write(id+" "+id2label[id]+"\n")