import os
from os.path import join
dump_dir = "/home/stan/espnet/egs2/stop/big_superb/dump/raw/test/"
prompt_file = open(join(dump_dir, 'prompt'), 'r')
label_file = open(join(dump_dir, 'label'), 'r')
text_file = open(join(dump_dir, 'text'), 'r')

prompt, label, text = prompt_file.readlines(), label_file.readlines(), text_file.readlines()
count, init = 0, 0
for i, (p, l, t) in enumerate(zip(prompt, label, text)):
    p, l, t = p.split()[0], l.split()[0], t.split()[0]
    if not (p == l and l == t):
        if count == 0:
            init = i
            print(i)
            print(f"prompt: {p}, label: {l}, text: {t}")
        count += 1
print("unmatch total ", count)
print("Init ", init)

