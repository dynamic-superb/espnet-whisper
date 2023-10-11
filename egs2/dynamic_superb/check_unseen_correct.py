import os

unseen_file_name = '/home/stan/espnet/egs2/stop/big_superb/dump/raw/test/unseen'
unseen_file = open(unseen_file_name, 'r').readlines()

exist_file = set()
count = 0
for line in unseen_file:
    [file_key, _] = line.split()
    assert file_key.strip() not in exist_file, file_key
    exist_file.add(file_key.strip())
    count += 1
assert len(exist_file) == count
print(exist_file)
print(f"{unseen_file_name} is correct")