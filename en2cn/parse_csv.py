import csv
import string
import json

#fields = ['word', 'phonetic', 'definition', 'translation', 'pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 'exchange', 'detail', 'audio']

# empty_fields = ['pos', 'collins', 'oxford', 'tag', 'bnc', 'frq', 'exchange', 'detail', 'audio']

empty_fields = ['pos', 'audio', 'detail']
need_fields = ['word', 'definition', 'translation', 'tag', 'exchange']
pos = ['n.', 'a.', 'vt.', 'vi.', 'v.', 'abbr.', 'int.', 'num.', 'interj.', 'adj.', 'adv.', 'pron.', 'un.', 'na.', 'pl.', 'conj.', 'art.', 'prep.', 'vi.vt.', 'pr.', 'vt.vi.', 'aux.', 'pp.']
v_pos = ['vt.', 'vi.', 'v.', 'vi.vt.', 'vt.vi.', 'aux.', 'pp.']
n_pos = ['n.', 'pl.']
adj_pos = ['adj.']

def filter_csv():
  with open('ecdict.csv', newline='') as csvfile:
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
        exchange = row['exchange']
        if exchange != '':
          _info = exchange.split('/')
          info = {}
          for _i in _info:
            k,v = _i.split(':')
            info[k] = v
          v_extension = {}
          n_extension = {}
          adj_extension = {}
          v_variations = {'formats': []}
          n_variations = {'formats': []}
          adj_variations = {'formats': []}
          for k,v in info.items():
            if k in ['p', 'd', 'i', '3']:
              v_extension[k] = v
            if k in ['s']:
              n_extension[k] = v
            if k in ['r', 't']:
              adj_extension[k] = v
            if k in ['0']:
              v_variations['origin'] = v
              n_variations['origin'] = v
              adj_variations['origin'] = v
            if k in ['1']:
              for _v in v:
                if _v in ['p', 'd', 'i', '3']:
                  v_variations['formats'].append(_v)
                if _v in ['r', 't']:
                  adj_variations['formats'].append(_v)
                if k in ['s']:
                  n_variations['formats'].append(_v)
          for ex in explanation:
            if ex['pos'] in v_pos and v_extension != {}:
              ex['extension'] = v_extension
            if ex['pos'] in n_pos and n_extension != {}:
              ex['extension'] = n_extension 
            if ex['pos'] in adj_pos and adj_extension != {}:
              ex['extension'] = adj_extension
            if ex['pos'] in v_pos and v_variations['formats'] != []:
              ex['variations'] = v_variations
            if ex['pos'] in n_pos and n_variations['formats'] != []:
              ex['variations'] = n_variations
            if ex['pos'] in adj_pos and adj_variations['formats'] != []:
              ex['variations'] = adj_variations
          #print(e)
        final.append(e)
          #print(variations)
          #print(info)
    return final

def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

re = filter_csv()
writeTo('here.json', re)
#print(re)
#print(len(re))
