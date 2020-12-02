# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:47:32 2020

@author: adnane
"""
import os 
import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
from doc_to_sentences import text_to_sentences

folder = 'data'
filenames = os.listdir(folder)
paths = [os.path.join(folder, filename) for filename in filenames]

res_dict = text_to_sentences(paths)

df_countries = pd.read_csv('resources/countries_code.csv')
df_countries.name = df_countries.name.str.lower()
df_countries.alpha2 = df_countries.name.str.lower()
df_countries.alpha3 = df_countries.name.str.lower()
country_list = list(df_countries.name) + list(df_countries.alpha2) + list(df_countries.alpha3)

df_list = []

def stem(tokenized_sentence):
    porter = PorterStemmer()
    res = [porter.stem(w) for w in tokenized_sentence]
    return(res)

def remove_punct(sentence_string, punct = '''!"'(),-.:;?)'''):
    return(''.join([char if char not in punct else ' ' for char in sentence_string]))
    
for path in paths:
    df_temp = pd.DataFrame()
    df_temp['sentence'] = res_dict[path]
    df_temp['path'] = path
    df_temp.sentence = df_temp.sentence.str.lower()
    df_temp.sentence = df_temp.sentence.apply(remove_punct)
    df_temp.sentence = df_temp.sentence.str.split()
#    df_temp.sentence = df_temp.sentence.apply(stem)
    df_list.append(df_temp)
    
df = pd.concat(df_list)

question_key_words ={
        1: [[['personal'], ['data']]],
        2: [[['data'], ['processing'], ['agreement', 'addendum']]],
        3: [[['transfer','access'], ['outside'], ['eu','european union']]],
        4: [[['transfer','access'], ['outside'], ['eu','european'], country_list]],     
        8: [[['bcr', 'scc', 'rules', 'clauses']]],
        13:[[['iso27001']],[['iso', '27001']]],
        14:[[['cost']]],
        15:[[['third'],['parties']], [['contractors']]],
        16:[[['third'],['parties'],['because']], [['contractors'],['because']]],
        17:[[['third'],['parties'],['because']], [['contractors'],['because']]],
        21:[[['audit']]],
        22:[[['data'],['period']]],
        23:[[['data'],['period'],['days','months','years','weeks']]] # cas échéant de la question 22
        }

#for question_id in question_key_words:
#    answers = question_key_words[question_id]
#    answers = [stem(keyword_list) for answer in answers for keyword_list in answer]
#    question_key_words[question_id] = answers
#        

#Listing question ids 
questions = list(question_key_words)
questions.sort()
questions = [q for q in questions if q<=22]

estimates = []
for question_id in question_key_words:
    answer_list = question_key_words[question_id]
    answers = [any(any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer) for answer in answer_list) for sentence in df.sentence) for df in df_list]
    estimates.append(answers)

estimates = np.array(estimates)
estimates = estimates.astype(int)

# Cas échéant de la question 22
estimates[-2] = estimates[-1] + estimates[-2]
estimates = estimates[:-1]

# =============================================================================
# load true answers
# =============================================================================

train_df = pd.read_csv('resources/train.csv')
train_df['question_number_aux'] = train_df.question_number.mod(22)
train_df.loc[train_df['question_number_aux']==0,'question_number_aux'] = 22 

targets = []
for question_id in question_key_words:
    if question_id<=22:
        answer_list = list(train_df[train_df['question_number_aux'] == question_id].response_id)
        targets.append(answer_list)
targets = np.array(targets)

n_samples = targets.shape[1]
question_to_acc_map_baseline = {}
baseline = np.array([[np.bincount(x).argmax() for x in targets]] * targets.shape[1]).T
for row in range(targets.shape[0]):
    acc = 1 - np.count_nonzero(targets[row] - baseline[row])/n_samples
    question_to_acc_map_baseline[questions[row]] = acc

question_to_acc_map = {}

for row in range(targets.shape[0]):
    acc = 1 - np.count_nonzero(targets[row] - estimates[row])/n_samples
    question_to_acc_map[questions[row]] = acc

print()
print('Regexp')
print(question_to_acc_map)

print()
print('Baseline: prédiction = réponse la plus fréquente')
print(question_to_acc_map_baseline)

