import argparse
from collections import defaultdict
import json
import tqdm
Inference_Tasks = open("test_tasks.txt", 'r').readlines()
Inference_Tasks = [t.strip().replace('\n','') for t in Inference_Tasks]
howfarareyou = open('/home/stan/espnet/egs2/stop/big_superb/howfarareyou.txt', 'r').readlines()
howfarareyou = set(l.strip()+'-'+l.strip() for l in howfarareyou)
sarcasm = open('/home/stan/espnet/egs2/stop/big_superb/SarcasmDetection_Mustard.txt', 'r').readlines()
sarcasm = set(l.strip()+'-'+l.strip() for l in sarcasm)
language = open('/home/stan/espnet/egs2/stop/big_superb/LanguageIdentification_VoxForge.txt', 'r').readlines()
language = set(l.strip()+'-'+l.strip() for l in language)
Dialogue = open('/home/stan/espnet/egs2/stop/big_superb/DialogueActPairing_DailyTalk.txt', 'r').readlines()
Dialogue = set(l.strip()+'-'+l.strip() for l in Dialogue)


parser = argparse.ArgumentParser(description="Macro-F1 for intent classification")
parser.add_argument("--hyp_trn", required=True, help="hyp.trn file path")
parser.add_argument("--ref_trn", required=True, help="ref.trn file path")
parser.add_argument("--split", default="test", help="Split: train, validation, test")
parser.add_argument("--output_file", default="whisper.csv", help="output file path")
args = parser.parse_args()
print(args)


def compute_precision_recall_f1(count_metrics):
    tp = count_metrics["TP"]
    fp = count_metrics["FP"]
    fn = count_metrics["FN"]
    precision = 0.0 if tp == 0 else float(tp) / float(tp + fp)
    recall = 0.0 if tp == 0 else float(tp) / float(tp + fn)
    if precision == 0.0 or recall == 0.0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    return f1


if __name__ == "__main__":
    metrics = defaultdict()
    correct, total = 0, 0
    # Inference_Tasks = open('local/task_list.txt', 'r').readlines()
    file = open(args.output_file, 'w')
    unseen = open(f"dump/raw/{args.split}/unseen", 'r').readlines()
    unseen = [r.split(maxsplit=1) for r in unseen]
    unseen_table = {}
    for f, v in unseen:
        unseen_table[f"{f}-{f}"]  = bool(int(v.replace('\n','')) )
    # print(unseen)
    table = {t:{'correct': 0, 'total':0, 'seen_correct': 0, 'seen_total':0, 'unseen_correct': 0, 'unseen_total':0} for t in Inference_Tasks}
    with open(args.hyp_trn, "r") as hyp, open(args.ref_trn, "r") as ref:
        for line_hyp, line_ref in tqdm.tqdm(zip(hyp, ref), total=len(unseen)):
            line_hyp, line_ref = line_hyp.split('('), line_ref.split('(')
            assert line_hyp[-1] == line_ref[-1], line_hyp
            try:
                assert line_hyp[-1].replace('(', '').replace(')','').strip() in unseen_table.keys(), line_hyp[-1].replace('(', '').replace(')','').strip()
            except:
                continue
            unseen = unseen_table[line_hyp[-1].replace('(', '').replace(')','').strip()]
            for task in table.keys():
                if task in line_hyp[-1] or line_hyp[-1].replace('(', '').startswith('0906_data_test') or line_hyp[-1].replace('(', '').startswith('0909_data_test'):
                    if line_hyp[-1].replace('(', '').replace(')','').strip() in howfarareyou:
                        task = "HowFarAreYou_3DSpeaker"
                    elif line_hyp[-1].replace('(', '').replace(')','').strip() in sarcasm:
                        task = "SarcasmDetection_Mustard"
                    elif line_hyp[-1].replace('(', '').replace(')','').strip() in Dialogue:
                        task = "DialogueActPairing_DailyTalk"
                    elif line_hyp[-1].replace('(', '').replace(')','').strip() in language:
                        task = "LanguageIdentification_VoxForge"
                    else:
                        task = task
                    predicted_intent, actual_intent = line_hyp[0], line_ref[0]
                    if predicted_intent.strip() == actual_intent.strip():
                        table[task]['correct'] += 1
                        correct += 1
                    table[task]['total'] += 1
                    if unseen:
                        table[task]['unseen_total'] += 1
                        if predicted_intent.strip() == actual_intent.strip():
                            table[task]['unseen_correct'] += 1
                    else:
                        table[task]['seen_total'] += 1
                        if predicted_intent.strip() == actual_intent.strip():
                            table[task]['seen_correct'] += 1
                        
                    break
                
                
            total += 1
    print(f"The Accuray: {correct*100 / total}%")
    json.dump(table, open(args.output_file.replace('.csv', '.json'), 'w'))
    # table = sorted([(k, v['correct']/v['total'],v['correct'], v['total']) for k,v in table.items() if v['total'] > 0])
    file.write('Inference Tasks, Acc, Seen_Acc, Unseen_Acc, Total, Seen_Total, Unseen_Total \n')
    for t in Inference_Tasks:
        t = t.strip()
        v = table[t]
        if v['total'] > 0:
            acc, total = v['correct']/v['total'], v['total']
            acc = f"{acc*100:.2f}%"
        else:
            acc = ""
            print(f"{t}: Total = 0")
        if v['seen_total'] > 0:
            seen_acc,  seen_total = v['seen_correct']/v['seen_total'], v['seen_total']
            seen_acc = f"{seen_acc*100:.2f}%"
        else:
            seen_acc,  seen_total = "", v['seen_total']
            
        if v['unseen_total'] > 0:
            unseen_acc, unseen_total = v['unseen_correct']/v['unseen_total'], v['unseen_total']
            unseen_acc = f"{unseen_acc*100:.2f}%"
        else:
            unseen_acc, unseen_total = "", v['unseen_total']
            
        file.write(f'{t}, {acc}, {seen_acc}, {unseen_acc}, {total}, {seen_total}, {unseen_total} \n')
        

