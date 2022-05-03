import glob


metadata_dict = {}
counter = 0

for file in glob.glob("data/*.metadata"):
  with open(file) as f:
    cur_dict = {}
    for l in f:
      cur_l = l.strip().split()
      k = cur_l[0]
      if k == 'SES':
        cur_SES = " ".join(cur_l[1:])
      elif k == 'LBD':
        cur_LBD = " ".join(cur_l[1:])
      elif k in ['SCD', 'SEX', 'AGE', 'ACC', 'ACT', 'BIR']:
        v = " ".join(cur_l[1:])
        cur_dict[k] = v

    if cur_SES in metadata_dict:
      metadata_dict[cur_SES][cur_LBD] = cur_dict
    else:
      metadata_dict[cur_SES] = {cur_LBD: cur_dict}

    counter += 1

print(len(metadata_dict))

for k in metadata_dict.keys():
  cur_vs = metadata_dict[k].values()
  print(set([elem['AGE'] for elem in cur_vs]))
  # print(set([elem['ACT'] for elem in cur_vs]))
  # print(set([elem['BIR'] for elem in cur_vs]))
  print()