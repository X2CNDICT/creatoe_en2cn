from pymongo import MongoClient
import json
import os
import copy

class DB:
  def __init__(self, dbname, user, password, host, authdb='admin'):
    from urllib.parse import quote_plus
    uri = "mongodb://{}:{}@{}/{}".format(quote_plus(user), quote_plus(password), host, authdb)
    self.client = MongoClient(uri)
    self.db = self.client[dbname]
    self.vocabs = self.db.vocabs
    self.base = self.db.base
    self.verb_extension =  self.db.verbs_extension
    self.noun_extension = self.db.noun_extension
    self.adj_extension = self.db.adj_extension

  def bulk_create_vocabs(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.insert_vocabs_one(e)
      print("{} records have been created in base".format(self.vocabs.count()))

  def bulk_create_base(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.insert_base_one(e)
      print("{} records have been created in base".format(self.base.count()))

  def bulk_create_noun_ext(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.noun_extension.insert_one(e)
      print("{} records have been created in noun extension".format(self.noun_extension.count()))

  def bulk_create_adj_ext(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.adj_extension.insert_one(e)
      print("{} records have been created in adj extension".format(self.adj_extension.count()))

  def bulk_create_verb_ext(self, dictionary_json_file):
    with open(dictionary_json_file) as f:
      content = json.load(f)
      for e in content:
        self.verb_extension.insert_one(e)
      print("{} records have been created in verb extension".format(self.verb_extension.count()))

  def cleanup_vocabs(self):
    self.vocabs.drop()

  def cleanup_base(self):
    self.base.drop()
  
  def cleanup_verb_ext(self):
    self.verb_extension.drop()

  def cleanup_adj_ext(self):
    self.adj_extension.drop()
  
  def cleanup_noun_ext(self):
    self.noun_extension.drop()

  def insert_vocabs_one(self, e):
    db_e = self.vocabs.find_one({"word": e["word"]})
    print(e)
    if db_e == None:
      self.vocabs.insert_one(e)
    else:
      explanation = copy.deepcopy(db_e["explanation"])
      explanation.extend(e["explanation"])
      self.vocabs.update_one({"word": e["word"]}, {"$set": {"explanation": explanation}})

  def insert_base_one(self, e):
    db_e = self.base.find_one({"word": e["word"]})
    print(e)
    if db_e == None:
      self.base.insert_one(e)
    else:
      explanation = copy.deepcopy(db_e["explanation"])
      explanation.extend(e["explanation"])
      self.base.update_one({"word": e["word"]}, {"$set": {"explanation": explanation}})

  def search_base(self, text):
    return [e for e in self.base.find({"word": text})]

  #def search_base_by_pos(self, pos):
  #  return [e for e in self.base.find({'explanation.pos': pos})]
  
  #def search_base_by_meaning_pos(self, meaning, pos):
  #  return [e for e in self.base.find({'explanation.meaning': {"$regex": meaning}, "explanation.pos": pos})]

  #def update_base_explanation(self, o_id, explanation, word):
  #  self.base.replace_one({"_id": o_id}, {"explanation": explanation, "word": word})

