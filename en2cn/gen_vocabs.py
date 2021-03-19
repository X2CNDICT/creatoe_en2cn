import json
import re
import copy

v_pos = ['vt.', 'vi.', 'v.', 'vi.vt.', 'vt.vi.', 'aux.', 'pp.']
n_pos = ['n.', 'pl.']
adj_pos = ['adj.', 'a.']


def loadjson(filename):
  data = []
  with open(filename) as f:
    data = json.load(f)
  return data

def printjson(filename):
  with open(filename) as f:
    data = json.load(f)
    for e in data:
      print(e)



n_extensions = loadjson('./middle/noun_variations.json')
adj_extensions = loadjson('./middle/adjs_variations.json')
verb_1_extensions = loadjson('./middle/verbs_1_variations.json')
verb_2_extensions = loadjson('./middle/verbs_2_variations.json')
adj_inverse_extensions = loadjson('./middle/adjs_inverse_variations.json')


def search_extension(extensions, word):
  ne = None
  if word in extensions:
    ne = extensions[word] 
  return ne

def analyze_pure(purefile):
  new_data = []
  new_n_data = []
  new_adj_data = []
  new_verb_1_data = []
  new_verb_2_data = []
  with open(purefile, 'r') as f:
    data = json.load(f)
    for r in data:
      word = r["word"]
      _r = {
        "word": word,
        "explanation": []
      }
      for ex in r['explanation']:
        if ex["pos"] in n_pos:
          ne = search_extension(n_extensions, word)
          if ne != None and ne[0][-1] == "s" and ne[0][-2:] != "ss" and '人名' not in ex["meaning"]:
            extension = {"singular": word, "plural": ne[0]}
            _new_ex = {
              "pos": ex["pos"],
              "meaning": ex["meaning"],
              "extension": extension,
            }
            _r["explanation"].append(_new_ex)

            new_ex = copy.deepcopy(_new_ex)
            new_ex["variations"] = {"original": word, "formats": ["plural"]}
            new_r = {"word": ne[0], "explanation": [new_ex]}
            new_n_data.append(new_r)
          else:
            _r["explanation"].append(ex)

        elif ex["pos"] in adj_pos:
          ne = search_extension(adj_extensions, word)
          inverse_ne = search_extension(adj_inverse_extensions, word)
          ex["pos"] = "adj." # remove "a."
          if ne != None and ne[0][-2:] == 'er' and ne[1][-3:] == "est":
            extension = {"original": word, "comparative": ne[0], "superlative": ne[1]}
            _new_ex = {
              "pos": ex["pos"],
              "meaning": ex["meaning"],
              "extension": extension,
            }
            _r["explanation"].append(_new_ex)
          elif inverse_ne != None:
            _ne = search_extension(adj_extensions, inverse_ne[0])
            if _ne != None and _ne[0][-2:] == "er" and _ne[1][-3:] == "est":
              assert(word == _ne[0] or word == _ne[1])
              extension = {"original": inverse_ne[0], "comparative": _ne[0], "superlative": _ne[1]}
              _new_ex = {
                "pos": ex["pos"],
                "meaning": ex["meaning"],
                "extension": extension,
              }
              form = "comparative" if _ne[0] == word else "superlative"
              _new_ex["variations"] = {"original": inverse_ne[0], "formats": [form]}    
              _r["explanation"].append(_new_ex)
            else:
              _r["explanation"].append(ex)
          else:
            _r["explanation"].append(ex)
        elif ex["pos"] in v_pos:
          ne_1 = search_extension(verb_1_extensions, word)
          ne_2 = search_extension(verb_2_extensions, word)
          if ne_2 != None:
            extension = {"original": word}
            for test in ne_2:
              if test[-1] == 's':
                extension["3"] = test
              elif test[-1] == 'g':
                extension["present_participle"] = test
              elif test[-1] == 'd':
                extension["past_tense"] = test
              else:
                extension["past_participle"] = test
            _new_ex = {
              "pos": ex["pos"],
              "meaning": ex["meaning"],
              "extension": extension,
            }
            _r["explanation"].append(_new_ex)

            if "3" in extension:
              new_ex = copy.deepcopy(_new_ex)

              new_ex["variations"] = {"original": word, "formats": ["3"]}
              new_r = {"word": extension["3"], "explanation": [new_ex]}
              new_verb_2_data.append(new_r)
            if "past_tense" in extension: 
              new_ex = copy.deepcopy(_new_ex)

              new_ex["variations"] = {"original": word, "formats": ["past_tense"]}
              new_r = {"word": extension["past_tense"], "explanation": [new_ex]}
              new_verb_2_data.append(new_r)
            if "past_participle" in extension:
              new_ex = copy.deepcopy(_new_ex)

              new_ex["variations"] = {"original": word, "formats": ["past_participle"]}
              new_r = {"word": extension["past_participle"], "explanation": [new_ex]}
              new_verb_2_data.append(new_r)
            if "present_participle" in extension:
              new_ex = copy.deepcopy(_new_ex)

              new_ex["variations"] = {"original": word, "formats": ["present_participle"]}
              new_r = {"word": extension["present_participle"], "explanation": [new_ex]}
              new_verb_2_data.append(new_r)
          elif ne_1 != None:
            extension = {"original": word}
            for test in ne_1:
              if test[-1] == 's':
                extension["3"] = test
              elif test[-1] == 'g':
                extension["present_participle"] = test
              elif test[-1] == 'd':
                extension["past_tense"] = test
                extension["past_participle"] = test
            _new_ex = {
              "pos": ex["pos"],
              "meaning": ex["meaning"],
              "extension": extension,
            }
            _r["explanation"].append(_new_ex)

            if "3" in extension:
              new_ex = copy.deepcopy(_new_ex)
              new_ex["variations"] = {"original": word, "formats": ["3"]}
              new_r = {"word": extension["3"], "explanation": [new_ex]}
              new_verb_1_data.append(new_r)
            if "present_participle" in extension:
              new_ex = copy.deepcopy(_new_ex)
              new_ex["variations"] = {"original": word, "formats": ["present_participle"]}
              new_r = {"word": extension["present_participle"], "explanation": [new_ex]}
              new_verb_1_data.append(new_r)
            if "past_tense" in extension: 
              new_ex = copy.deepcopy(_new_ex)
              new_ex["variations"] = {"original": word, "formats": ["past_participle", "past_tense"]}
              new_r = {"word": extension["past_tense"], "explanation": [new_ex]}
              new_verb_1_data.append(new_r)
          else:
            _r["explanation"].append(ex)
        else:
          _r["explanation"].append(ex)
      new_data.append(_r)
  return (new_data, new_n_data, new_adj_data, new_verb_1_data, new_verb_2_data)


def writeTo(filename, content):
  with open(filename, 'w') as output:
    json.dump(content, output)

def validate_pure():
  #pattern = re.compile('[a-zA-Z-\.\ ]*')
  final = []
  with open('./middle/pure.json', 'r') as f:
    data = json.load(f)
    for r in data:
      word = r["word"]
      if word[-1] == "?":
        pass
      else:
        if word[0] == "'":
          r["word"] = word.replace("'", "")
        final.append(r)
  import os
  if not os.path.exists('final'):
    os.makedirs('final')
  writeTo('./final/vocabs_base.json', final)


def process_pure():
  results = analyze_pure('./final/vocabs_base.json')

  writeTo('./final/vocabs_base.json', results[0])
  writeTo('./final/vocabs_n_ext.json', results[1])
  writeTo('./final/vocabs_adj_ext.json', results[2])
  writeTo('./final/vocabs_verb_1_ext.json', results[3])
  writeTo('./final/vocabs_verb_2_ext.json', results[4])

if __name__ == "__main__":
  validate_pure()
  process_pure()
  #printjson('./final/base.json')
  #printjson('./final/n_ext.json')
  #printjson('./final/adj_ext.json')
  #printjson('./final/verb_1_ext.json')
  #printjson('./final/verb_2_ext.json')




