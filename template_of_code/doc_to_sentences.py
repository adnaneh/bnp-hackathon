#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:31:24 2020

@author: jores
"""

"""
Created on Tue Dec  1 11:05:03 2020
@author: adnane
"""
import sys
import os
import io
import re
from unicodedata import category
import seaborn as sns
import matplotlib.pyplot as plt

#sentence_end_punctuation = '((?<!N.)(((?<=[\.\?\!\;])(?= [A-Z]))|((?<=[\.\?\!\;])(?=(\s)*\n))))'
sentence_end_punctuation = '((?<!N.)(((?<=[\.\?\!\;])(?= [A-Z]))|((?<=[\.\?\!\;])(?=(\s)*\n))))'
#sentence_end_return = '(?=\n[^a-zA-Z]*(?=[A-Z]|[a-z][A-Z]))'
usa_regexp = '\WU.S.A\W|\WU.S\W|\WUSA\W|\WUnited States\W'
uk_regexp = '\WUK\W|\WUnited Kingdom\W'
#table_regexp = '((\n[A-Z][\S ]*\t)|(\n([A-Z][\w -]*,(\s)+)+[A-Z][\w -]*\n))'
#table_regexp = '(\n([A-Z][a-zA-Z \-]*(,\s+|\t\s*))+[A-Z][a-zA-Z \-]*\n)'
#table_regexp = '((\n(([A-Z][a-zA-Z\-\.]+( ){0,1}){1,5}(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}){2,})'
# [(.)\n]*(\n\n|\Z)
#table_regexp = '((\n(([A-Z][a-zA-Z\-\.]+( ){0,1})+(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\.]+( ){0,1})+){1,})'
#table_regexp = '(\n([A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}(\n([A-Z]([a-zA-Z\-\.]+( ){0,1})+(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\.]+( ){0,1})+){1,})'
#table_regexp = '(\n(([A-Z][a-zA-Z\-\. ]+){1,5}(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\. ]+){1,5}\n)'
##table_regexp = '((\n([A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}(,[\t ]+|\t[\t ]*)){1,10}[A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5})(\n([A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}(,[\t ]+|\t[\t ]*)){1,10}[A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}))'
#table_regexp = '(([A-Z]([a-zA-Z\-\.]+( ){0,1}){1,5}(,[\t ]+|\t[\t ]*))+[A-Z]([a-zA-Z\-\. ]+){1,5})'

#table_regexp = '\n([A-Z][a-zA-Z ]*\t)+[a-zA-Z ]*\n((.)*\n)+\n\n'
#table_regexp = '\n[A-Z][a-zA-Z ]*\t)+[a-zA-Z ]*\n'
#table_regexp = re.compile(table_regexp, re.DOTALL)


chrs = (chr(i) for i in range(sys.maxunicode + 1))
all_punctuation = [c for c in chrs if category(c).startswith("P")]
natural_punctuation = '''!"'(),-.:;?'''
punctuation_to_filter = ''.join(
    [p for p in all_punctuation if p not in natural_punctuation])


def text_to_sentences(paths):
    res_dict = {}
    print('Séparation en phrase: regexp split (\.|\?|\!)\s(?![a-z])')
    print('Filtrage des charactères de ponctuation')
    print()

    for path in paths:
        #        d[path] = []
        print('Traitement de', path)
        with io.open(path, mode="r", encoding="utf-8") as f:
            text = f.read()

            sentences_filtered = re.split(sentence_end_punctuation, text)

            # Filtrages:
            sentences_filtered = [
                sentence for sentence in sentences_filtered if sentence != None]
            sentences_filtered = [re.sub('[' + re.escape(punctuation_to_filter) + ']',
                                         ' ', sentence).strip() for sentence in sentences_filtered]
            sentences_filtered = [re.sub(
                usa_regexp, ' usa ', sentence).strip() for sentence in sentences_filtered]
            sentences_filtered = [
                re.sub(uk_regexp, ' uk ', sentence).strip() for sentence in sentences_filtered]
            sentences_filtered = [re.sub('\s+', ' ', sentence)
                                  for sentence in sentences_filtered]
            sentences_filtered = [sentence for sentence in sentences_filtered if len(
                sentence) > 1 and any(c.isalpha() for c in sentence)]

        res_dict[path] = sentences_filtered

    print()
    print('Output pour chaque document stocké dans le dictionnaire res_dict')
    return res_dict


def get_statistic_text(res_dict):
    nb_sentences = []
    nb_words_per_sentences = []
    for elt, value in res_dict.items():
        nb_sentences.append(len(value))
        nb_words_per_sentences.extend([len(sent.split()) for sent in value])
    fig, ax = plt.subplots(1, 2, figsize=(10, 6))
    sns.distplot(nb_sentences, ax=ax[0], bins=50, kde=False)
    sns.distplot(nb_words_per_sentences, ax=ax[1])

    return fig, ax


if __name__ == '__main__':
    folder = 'data'
    filenames = os.listdir(folder)
    paths = [os.path.join(folder, filename) for filename in filenames]
    res_dict = text_to_sentences(paths)
    fig, ax = get_statistic_text(res_dict)
