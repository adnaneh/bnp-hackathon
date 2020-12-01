# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:05:03 2020

@author: adnane
"""
import sys
import os 
import io 
import re
from unicodedata import category

folder = 'data'

filenames = os.listdir(folder)
paths = [os.path.join(folder, filename) for filename in filenames]

res_dict = {}
sentence_end_punctuation = '((?<![A-Z][a-zA-Z][a-zA-Z])(?<![A-Z][a-zA-Z])(?<![A-Z])(?<!\sno)(?=\.|\?|\!)\s(?![a-z]))'
sentence_end_return = '(\n[^a-zA-Z]*(?=[A-Z]|[a-z][A-Z]))'
chrs = (chr(i) for i in range(sys.maxunicode + 1))
all_punctuation = [c for c in chrs if category(c).startswith("P")]
natural_punctuation = '!"\'(),-.:;?'
punctuation_to_filter = ''.join([p for p in all_punctuation if p not in natural_punctuation])


print('Séparation en phrase: regexp split (\.|\?|\!)\s(?![a-z])')
print('Filtrage des charactères de ponctuation')
print()
for path in paths:
    print('Traitement de', path)
    with io.open(path, mode="r", encoding="utf-8") as f:
        text = f.read()
        
        # Séparation en phrases
        sentences_filtered = re.split(sentence_end_punctuation +'|' + sentence_end_return, text)
        
        # Filtrages:    
        sentences_filtered = [sentence for sentence in sentences_filtered if sentence!=None]
        sentences_filtered = [re.sub('['+ punctuation_to_filter + ']', ' ', sentence).strip() for sentence in sentences_filtered]
        sentences_filtered = [sentence for sentence in sentences_filtered if len(sentence)>1 and any(c.isalpha() for c in sentence)]
                
    res_dict[path] = sentences_filtered

print()
print('Output pour chaque document stocké dans le dictionnaire res_dict')

    
