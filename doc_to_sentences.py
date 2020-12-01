# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:05:03 2020

@author: adnane
"""
import sys
import os 
import io 
import string
import re
from unicodedata import category

folder = 'data'

filenames = os.listdir(folder)
paths = [os.path.join(folder, filename) for filename in filenames]

res_dict = {}
sentence_end_punctuation = '(?<![A-Z][a-zA-Z][a-zA-Z])(?<![A-Z][a-zA-Z])(?<![A-Z])(\.|\?|\!)\s(?![a-z])'
sentence_end_punctuation_or_return = '(?<![A-Z][a-zA-Z][a-zA-Z])(?<![A-Z][a-zA-Z])(?<![A-Z])((\.|\?|\!)\s(?![a-z])|\n\s*[A-Z])'
chrs = (chr(i) for i in range(sys.maxunicode + 1))
punctuation = ''.join([c for c in chrs if category(c).startswith("P")])

print('Séparation en phrase: regexp split (\.|\?|\!)\s(?![a-z])')
print('Filtrage des charactères de ponctuation: '+ string.punctuation)
print()
for path in paths:
    print('Traitement de', path)
    with io.open(path, mode="r", encoding="utf-8") as f:
        text = f.read()
        # Séparation en phrases
        text_split = re.split(sentence_end_punctuation, text)
        # Filtrage de la ponctuation, charactères :    
        text_split_filtered = [re.sub('['+ punctuation + ']', '', text).strip() for text in text_split] 
        text_split_filtered = [text for text in text_split_filtered if len(text)>0]
    res_dict[path] = text_split_filtered

print()
print('Output pour chaque document stocké dans le dictionnaire res_dict')
