# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 21:58:52 2020

@author: adnane
"""

from nltk.stem.porter import PorterStemmer


def stem(tokenized_sentence):
    porter = PorterStemmer()
    res = [porter.stem(w) for w in tokenized_sentence]
    return(res)


def path_to_name(path):
    return(path.split('\\')[-1].split('.')[0])