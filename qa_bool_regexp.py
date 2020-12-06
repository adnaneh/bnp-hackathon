# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:47:32 2020

@author: adnane
"""
import os
import pandas as pd
import numpy as np
from doc_to_sentences import text_to_sentences
import config as c
from utils import stem, path_to_name
import itertools


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

    return(df, df_sentences, df_list, df_list_full_sentences)


def get_countries(answer_list, df, n_countries, countries, nationalities=False, df_full=[]):
    ''' Renvoie moins de n pays à partir d'une configuration de:
        - La configuration de réponse: answer_list
        - Les phrases du text contenues dans le dataframe df '''

    labels = [any(all(any(key_word in sentence for key_word in key_word_list)
                      for key_word_list in answer) for answer in answer_list) for sentence in df.sentence]
    df_extract = df[labels]
    if len(df_full) > 0:
        df_full_extract = df_full[labels]
    country_extract = [[word for word in sentence if word in countries]
                       for sentence in df_extract.sentence]
    answer_country = list(set(itertools.chain.from_iterable(country_extract)))
    codes = [c.df_countries.loc[c.df_countries.name == country, 'id'].iloc[0]
             for country in answer_country]
    codes.sort()
    country_codes = [0] * n_countries
    for i in range(min(len(codes), n_countries)):
        country_codes[i] = codes[i]
    if len(df_full) > 0:
        return(answer_country, list(df_full_extract.sentence), country_codes)
    else:
        return(answer_country, None, country_codes)


def regexp_pred_countries(df_list):
    res = [[] for i in range(len(df_list))]
    for question_id in c.country_question_key_words:
        question_args = c.country_question_arguments[question_id]
        for df_i in range(len(df_list)):
            question_args['df'] = df_list[df_i]
            answer_countries, full_sentences, country_codes = get_countries(
                **question_args)
            res[df_i].extend(country_codes)
    return(np.array(res).T)


def regexp_pred(df_list, df_list_full_sentences=None):
    question_key_words = c.question_key_words

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
if __name__ == '__main__':
    folder = 'data'
    filenames = os.listdir(folder)
    paths = [os.path.join(folder, filename) for filename in filenames]
#    paths = [paths[0]]

    res_dict = text_to_sentences(paths)
    df, df_sentences, df_list, df_list_full_sentences = pre_processing(
        res_dict, paths)
    estimates, question_key_words = regexp_pred(df_list)

    train_df = pd.read_csv('resources/train.csv')
    train_df['question_number_aux'] = train_df.question_number.mod(22)
    train_df.loc[train_df['question_number_aux']
                 == 0, 'question_number_aux'] = 22

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
    documents = np.where(
        (targets[question_num] - estimates[question_num]) != 0)[0] + 1

    print('Documents avec faute', [paths[d - 1] for d in documents])

    # =============================================================================
    # Pays
    # =============================================================================

#    question_id = 11
# for question_id in c.country_question_arguments:
#    question_args = c.country_question_arguments[question_id]
#    results_countries = {}
#    results_sentences = {}
#    for df_i in range(len(df_list)):
#        name = path_to_name(df_list[df_i].iloc[0].path)
#        question_args['df'] = df_list[df_i]
#        question_args['df_full'] = df_list_full_sentences[df_i]
#        answer_countries, full_sentences, country_codes= get_countries(**question_args)
#        results_countries[name] = answer_countries
#        results_sentences[name] = list(full_sentences)
#
#    question_args['answer_list']

    res = regexp_pred_countries(df_list)
    #sentences = [['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']]
    #sentence = ['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']
    #labels = [all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer) for answer in answer_list]
    #x = df[labels]
