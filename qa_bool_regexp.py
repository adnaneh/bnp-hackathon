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
import config as c


def stem(tokenized_sentence):
    porter = PorterStemmer()
    res = [porter.stem(w) for w in tokenized_sentence]
    return(res)


def remove_punct(sentence_string, punct='''!"'(),-.:;?)'''):
    return(''.join([char if char not in punct else ' ' for char in sentence_string]))



def pre_processing(res_dict, paths):

    df_list = []
    df_list_full_sentences = []

    for path in paths:
        df_temp = pd.DataFrame()
        df_temp['sentence'] = res_dict[path]
        df_temp['path'] = path
        df_list_full_sentences.append(df_temp.copy())
        df_temp.sentence = df_temp.sentence.str.lower()
        df_temp.sentence = df_temp.sentence.apply(remove_punct)
        df_temp.sentence = df_temp.sentence.str.split()
        df_temp.sentence = df_temp.sentence.apply(stem)
        df_list.append(df_temp)
    
    df = pd.concat(df_list)
    df_sentences = pd.concat(df_list_full_sentences)
    
    return(df, df_sentences, df_list)

def regexp_pred(df_list):
    question_key_words = {
        1: [[['personal'], ['data', 'information']]],
        2: [[['data'], ['processing'], ['agreement', 'addendum', 'terms']],
            [['dpa']]],
        3: [[['data','information'],['transfer', 'access'], ['outside']],
            [['transfer', 'access'], ['other'],['countries']],
    #        [['transfer', 'access'], ['outside'], ['eu', 'european', 'eea']],
            [['data','information'],['transfer', 'access'], c.non_eu_countries],
            [['data','information'],['transfer', 'access'], ['united'],['states']]],
        4: [[['data','information'],['transfer', 'access'], c.non_eu_countries]],
        8: [[['bcr', 'scc']],
            [['binding'], ['corporate'],['rules']],
            [['standard'], ['contractual'],['clauses']]],       
        13: [[['iso27001']],
             [['iso', '27001']]], #TODO include the name of the software in the sentence
        14: [[['cost', 'price']]],
        15: [[['data', 'information'],['third'], ['parties']],
             [['data', 'information'],['contractors']]],
        16: [[['cloud'],['service'],['provider']],
             [['monitoring'], ['services']],
             [['application'] ,['monitoring']],
             [['error'],['tracking']],
             [['payment'] ,['processor']],
             [['marketing'], ['automation'], ['software']],
             [['business'],['analytics']],
             [['crm']],
             [['set','below'],['parties']]
             ],
        17: [[['third'], ['parties'], ['listed']],
             [['sub'], ['contractors'], ['listed']],
             [['sub'], ['processors'], ['listed']],
             [['subprocessors'], ['listed']]
             ],
        21: [[['audit']]],
        22: [[['data'], ['retention']]], #TODO complete in details
        # cas échéant de la question 22
        23: [[['data'], ['retention'], ['days', 'months', 'years', 'weeks']]]
    }
    
    for question_id in question_key_words:
        answers = question_key_words[question_id]
        answers = [[stem(keyword_list) for keyword_list in answer]
                   for answer in answers]
    
        question_key_words[question_id] = answers
    #
    
    # Listing question ids
    questions = list(question_key_words)
    questions.sort()
    questions = [q for q in questions if q <= 22]
    
    estimates = []
    for question_id in question_key_words:
        answer_list = question_key_words[question_id]
        answers = [any(any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer)
                           for answer in answer_list) for sentence in df.sentence) for df in df_list]
        estimates.append(answers)
    
    estimates = np.array(estimates)
    estimates = estimates.astype(int)
    
    # Cas échéant de la question 22
    estimates[-2] = estimates[-1] + estimates[-2]
    estimates = estimates[:-1]
    return(estimates, question_key_words)

# =============================================================================
# Evaluation
# =============================================================================

if __name__ == '__main__' :
    folder = 'data'
    filenames = os.listdir(folder)
    paths = [os.path.join(folder, filename) for filename in filenames]
#    paths = [paths[0]]
    
    res_dict = text_to_sentences(paths)
    df, df_sentences, df_list = pre_processing(res_dict, paths)
    estimates, question_key_words = regexp_pred(df_list)
    
    train_df = pd.read_csv('resources/train.csv')
    train_df['question_number_aux'] = train_df.question_number.mod(22)
    train_df.loc[train_df['question_number_aux'] == 0, 'question_number_aux'] = 22
    
    targets = []
    for question_id in c.boolean_questions:
        if question_id <= 22:
            answer_list = list(
                train_df[train_df['question_number_aux'] == question_id].response_id)
            targets.append(answer_list)
    targets = np.array(targets)
    
    n_samples = targets.shape[1]
    question_to_acc_map_baseline = {}
    baseline = np.array([[np.bincount(x).argmax()
                          for x in targets]] * targets.shape[1]).T
    for row in range(targets.shape[0]):
        acc = 1 - np.count_nonzero(targets[row] - baseline[row]) / n_samples
        question_to_acc_map_baseline[c.boolean_questions[row]] = acc
    
    question_to_acc_map = {}
    
    for row in range(targets.shape[0]):
        acc = 1 - np.count_nonzero(targets[row] - estimates[row]) / n_samples
        question_to_acc_map[c.boolean_questions[row]] = acc
    
    print()
    print('Regexp')
    print(question_to_acc_map)
    
    print()
    print('Baseline: prédiction = réponse la plus fréquente')
    print(question_to_acc_map_baseline)
    
    
    
    # =============================================================================
    # Etude des erreurs
    # =============================================================================
    question_id = 22
    
    print()
    print('Analyse question', question_id)
    
    answer_list = question_key_words[question_id]
    labels = [any(all(any(key_word in sentence for key_word in key_word_list)
                      for key_word_list in answer) for answer in answer_list) for sentence in df.sentence]
    x = df[labels]
    y = df_sentences[labels]
    
    question_num = c.boolean_questions.index(question_id)
    documents = np.where((targets[question_num] - estimates[question_num])!=0)[0] + 1
    
    print('Documents avec faute', [paths[d-1] for d in documents])
    #sentences = [['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']]
    #sentence = ['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']
    #labels = [all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer) for answer in answer_list]
    #x = df[labels]
