## Yomichan Frequency dictionary from .tsv file ##

# Dictionary consists of a zip file (named however you want) with two .json files inside:

# File 1: index.json
# The inside of this file looks like this:
# {"title":"Daily Conversation","format":3,"revision":"conversation.frequency"}
#  (you can modify the title as you want and the revision I followed the format XXX.frequency that I observed in other dictionaries

# File 2: term_meta_bank_1.json, generated using the following script:

import pandas as pd
import numpy
import json
import numpy

# Make sure the tsv file is on the same folder as the script to load the data correctly or update the path to it
data=pd.read_csv('./2_cejc_frequencylist_suw_token.tsv',sep='\t')
word_key = "語彙素" # this is where the words are stored on the .tsv
rank_key = "rank" # this is the column that is used as rank to make the dictionary, modify it to make other versions of the dictionary

# some words were empty so I removed those to avoid errors when importing into yomichan
data.replace("語彙素", numpy.nan, inplace=True)
data.dropna(subset=["語彙素"], inplace=True)

words = data[word_key].to_numpy()
ranks = data[rank_key].to_numpy()

# create dictionary to make json file
dict = []
for word, rank in zip(words, ranks):
    dict.append([word, "freq", rank])
    
# Serialization
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    
with open('./term_meta_bank_1.json', "w", encoding="utf-8") as f:
    json.dump(dict, f, cls=NpEncoder, ensure_ascii=False)
    
# to check if data is correctly formatted
# encoded json must follow format i.e. [["うん", "freq", 1], ["だ", "freq", 2]]
encodedNumpyData = json.dumps(dict, cls=NpEncoder, ensure_ascii=False)  # use dump() to write array into file
print(encodedNumpyData)