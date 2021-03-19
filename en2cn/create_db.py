from db import DB
if __name__ == '__main__':
  x2y = DB('en2cn', 'dict', 'turingmachine', '127.0.0.1')

  x2y.cleanup_base()
  x2y.bulk_create_base('./final/pure_base.json')

  x2y.cleanup_noun_ext()
  x2y.bulk_create_noun_ext('./final/pure_n_ext.json')

  x2y.cleanup_adj_ext()
  x2y.bulk_create_adj_ext('./final/pure_adj_ext.json')

  x2y.cleanup_verb_ext()
  x2y.bulk_create_verb_ext('./final/pure_verb_1_ext.json')
  x2y.bulk_create_verb_ext('./final/pure_verb_2_ext.json')


  x2y.cleanup_vocabs()
  x2y.bulk_create_vocabs('./final/vocabs_base.json')
  x2y.bulk_create_vocabs('./final/vocabs_n_ext.json')
  #x2y.bulk_create_vocabs('./final/vocabs_adj_ext.json')
  x2y.bulk_create_vocabs('./final/vocabs_verb_1_ext.json')
  x2y.bulk_create_vocabs('./final/vocabs_verb_2_ext.json')
