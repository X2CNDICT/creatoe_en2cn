import json

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

def analyze_variation():
  nouns, adjs, verbs_1, verbs_2 = {}, {}, {}, {}
  with open('./resources/variations.json', 'r') as f:
    data = json.load(f)
    for k,v in data.items():
      size = len(v)
      value = list(v.keys())
      # size == 1 possible noun
      if size == 1:
        nouns[k] = value
      # size == 2 possible adj
      if size == 2:
        adjs[k] = value
      # size == 3 possible verb
      if size == 3:
        verbs_1[k] = value
      # size == 4 possible verb
      if size == 4:
        verbs_2[k] = value
  import os
  if not os.path.exists('middle'):
    os.makedirs('middle')
  writeTo('./middle/noun_variations.json', nouns)
  writeTo('./middle/adjs_variations.json', adjs)
  writeTo('./middle/verbs_1_variations.json', verbs_1)
  writeTo('./middle/verbs_2_variations.json', verbs_2)

analyze_variation()

def analyze_inverse_variation():
  adjs = {}
  with open('./resources/inverse_variations.json', 'r') as f:
    data = json.load(f)
    for k,v in data.items():
      size = len(v)
      value = list(v.keys())
      if size == 1 and k[-2:] == "er":
        adjs[k] = value
      elif size ==1 and k[-3:] == "est":
        adjs[k] = value
  import os
  if not os.path.exists('middle'):
    os.makedirs('middle')
  writeTo('./middle/adjs_inverse_variations.json', adjs)

analyze_inverse_variation()
