# English to Chinese dictionary

The project aims to convert the dictionary content from [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT) into json file in bajiu dictionary format.


### Source content
  * `resources/ecdict.csv` from repo [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT)
  * `resources/variations.json` and `resources/inverse_variations.json`, which are generated through `stardict.py` from [skywind3000/ECDICT](https://github.com/skywind3000/ECDICT)
    ```
      def test7():
        lemma = LemmaDB()
        t = time.time()
        lemma.load('lemma.en.txt')
        print('load in %s seconds'%str(time.time() - t))
        variations = lemma._stems
        inverse_variations = lemma._words
        writeTo('variations.json', variations)
        writeTo('inverse_variation.json', inverse_variations)
    ```


### Parse content
  * `python parse_csv_pure.py` parse `resources/ecdict.csv` into `middle/pure.json`
  * `python parse_variations.py` parse `resources/variations.json` and `resources/inverse_variations.json` into 
    * `middle/adjs_inverse_variations.json`
    * `middle/adjs_variations.json`
    * `middle/noun_variations.json`
    * `middle/verbs_1_variations.json`
    * `middle/verbs_2_variations.json`


### Create TBR content
  * `python gen_pure.py` generates mongodb json files in `final/pure_*.json` from files in `middle`
  * `final/pure_*.json` will be stored in collection `base`, `verb_extension`, `adj_extension`, `noun_extension`.

### Create DB content
  * `python gen_vocabs.py` generates mongodb json files in `final/vocabs_*.json` from files in `middle`
  * `final/vocabs_*.json` will be stored in collection `vocabs`.

### Import data into mongodb
  * `reform_pos.sh` changes `vt.` into `v.vt.` and `vi.` into `v.vi.`, whose files are in `final`
  * `python create_db.py` inserts records into mongodb from `final`


