import csv
import string
import json

#fields = ['word', 'phonetic', 'definition', 'translation', 'pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 'exchange', 'detail', 'audio']

# empty_fields = ['pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 'exchange', 'detail', 'audio']

empty_fields = ['pos', 'audio', 'detail']
need_fields = ['word', 'definition', 'translation', 'tag', 'exchange']
pos = ['n.', 'a.', 'vt.', 'vi.', 'v.', 'abbr.', 'int.', 'num.', 'interj.', 'adj.', 'adv.', 'pron.', 'na.', 'pl.', 'conj.', 'art.', 'prep.', 'vi.vt.', 'pr.', 'vt.vi.', 'aux.', 'pp.']
v_pos = ['vt.', 'vi.', 'v.', 'vi.vt.', 'vt.vi.', 'aux.', 'pp.']
n_pos = ['n.', 'pl.']
adj_pos = ['adj.']

def filter_csv():
  with open('resources/ecdict.csv', newline='') as csvfile:
    dictreader = csv.DictReader(csvfile, delimiter=',')
    total = [row for row in dictreader]
    print(len(total))
    possible = [row for row in total if row['translation']!='' and row['word'][0]!='-' and row['word'][-1]!='-']
    print(len(possible))
    final = []
    for row in possible:
      for field in empty_fields:
        assert(row[field] == '' or row[field] == '""')
      explanation = [] 
      translation = row['translation'].split('\\n')
      for t in translation:
        _pos = t.split(' ')[0]
        _meaning = ' '.join(t.split(' ')[1:])
        if _pos in pos:
          explanation.append({'pos': _pos, 'meaning': _meaning})
      if len(explanation) > 0:
        e = {
          "word": row['word'],
          "explanation": explanation
        }
        final.append(e)
    return final

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

re = filter_csv()
print(len(re))
import os
if not os.path.exists('middle'):
  os.makedirs('middle')
writeTo('middle/pure.json', re)
#print(re)
#print(len(re))
