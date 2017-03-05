
# coding: utf-8

# In[12]:

import csv
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.text import Text
from collections import Counter
import pandas as pd
import openpyxl
import os
from textblob import TextBlob
import glob
import numpy as np
import pandas as pd
import re
import os


# In[13]:

#all texts in a directory the end with ".txt"
input_texts = glob.glob("*.txt")


# In[19]:

appended_data = []
for input_text in input_texts:
    #open each ".txt" file in a directory
    with open(input_text) as filehandle:
        #read text file
        txt = filehandle.read()
        #turn into blob
        blob = TextBlob(txt)
        
        #part-of-speech tag for every word
        taglist = blob.tags
        
        #every combination of trigram with part-of-speech tag
        pos_grams = list(zip(taglist[:-2], taglist[1:-1], taglist[2:]))
        
        #get only the adjectives that directly surround the word "america"
        america_grams = []
        for gram in pos_grams:
            if gram[1][0] == 'great':
                if gram[0][1].startswith("NN"):
                    america_grams.append(gram[0][0])
                elif gram [2][1].startswith("NN"):
                    america_grams.append(gram[2][0])
        
        #count the adjectives that directly surround "america"
        #clean_america_grams = [x.lower() for x in [america_grams]]
        clean_america_grams = [item.lower() for item in america_grams]
        modifier_count = Counter(clean_america_grams)
       
        #get the filename
        filename = os.path.split(input_text)[-1].replace(".txt","")
        
        #put the filename, adjective, and count in a list
        datalist = [(filename, token, count) 
                    for (token, count) in modifier_count.items()] 
        #put the datalist into a Pandas DataFrame
        tmp = pd.DataFrame(datalist if len(datalist) > 0 else None)
        appended_data.append(tmp)

#combine the DataFrame for every inaugural address into one DataFrame
appended_data = pd.concat(appended_data, axis=0)
#give the big DataFrame column names
appended_data.columns = ['president', 'word', 'count'] 
appended_data


# In[21]:

#write the big DataFrame to an Excel file
appended_data.to_csv('all_great_nouns.csv')


# In[ ]:



