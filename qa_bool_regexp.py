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
import re
from nltk.stem.porter import PorterStemmer


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
        
        # Regexps
        regexp = re.compile('([^a-zA-Z]|^)(Data|DATA) (Processing|PROCESSING) (Agreement|Addendum|AGREEMENT|ADDENDUM)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' dpad ')
        df_temp.sentence = df_temp.sentence.str.lower()
        
        regexp = re.compile('([^a-zA-Z]|^)cloud (service|services) provider(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' cloudserviceprovid ')       
        regexp = re.compile('([^a-zA-Z]|^)monitoring (service|services)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' monser ')   
        regexp = re.compile('([^a-zA-Z]|^)(application|performance|deployment) monitoring(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' appmon ')  
        regexp = re.compile('([^a-zA-Z]|^)(error|errors) tracking(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' errtrac ') 
        regexp = re.compile('([^a-zA-Z]|^)marketing automation(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' marketautomation ')  
        regexp = re.compile('([^a-zA-Z]|^)(business|product) analytics(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' businessanalytics ')  
        regexp = re.compile('([^a-zA-Z]|^)(image|images) hosting(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' imagehosting ')  
        regexp = re.compile('([^a-zA-Z]|^)(customer|customers) engagement(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' customerengagement ')  
        regexp = re.compile('([^a-zA-Z]|^)(digital|certified) signature(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' digitalsignature ')  
        regexp = re.compile('([^a-zA-Z]|^)(conversation|conversations) recording(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' conversationrecording ') 
        regexp = re.compile('([^a-zA-Z]|^)data warehouse(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' datawarehouse ')   
        regexp = re.compile('([^a-zA-Z]|^)(site|sites) search(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' sitesearch ')   
        regexp = re.compile('([^a-zA-Z]|^)support system(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' supportsystem ')   
        regexp = re.compile('([^a-zA-Z]|^)(events|event) ticketing(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' eventticketing ')   
        regexp = re.compile('([^a-zA-Z]|^)data visualization(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' datavisualization ')  
        regexp = re.compile('([^a-zA-Z]|^)intelligent search technology(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' intelligentsearchtechnology ')   
        regexp = re.compile('([^a-zA-Z]|^)intelligent analytics(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' intelligentanalytics ')
        regexp = re.compile('([^a-zA-Z]|^)authentication (systems|system)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' authenticationsystems ')   
        regexp = re.compile('([^a-zA-Z]|^)bill collection(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' billcollection ')   
        regexp = re.compile('([^a-zA-Z]|^)chat (services|service)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' chatservices ')   
        regexp = re.compile('([^a-zA-Z]|^)helpdesk (services|service)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' helpdeskservices ')    
        regexp = re.compile('([^a-zA-Z]|^)system administration (services|service)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' systemadministrationservices ')  
        regexp = re.compile('([^a-zA-Z]|^)exception reporting(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' exceptionreporting ')  
        regexp = re.compile('([^a-zA-Z]|^)customer relationship management(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' customerrelationshipmanagement ') 
        regexp = re.compile('([^a-zA-Z]|^)(subscription|referral) management(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' subscriptionmanagement ') 
        regexp = re.compile('([^a-zA-Z]|^)service provider(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' serviceprovider ') 
        
        regexp = re.compile('([^a-zA-Z]|^)data protection (law|laws)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' dataprolaw ') 
        
        regexp = re.compile('([^a-zA-Z]|^)english language(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' englanguage ') 
    
        regexp = re.compile('([^a-zA-Z]|^)user retention(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' userretention ') 
        
        regexp = re.compile('([^a-zA-Z]|^)eu( )*usa(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' euusa ') 
        regexp = re.compile('([^a-zA-Z]|^)usa( )*eu(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' euusa ') 
        regexp = re.compile('([^a-zA-Z]|^)swiss( )*usa(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' swissusa ') 
        regexp = re.compile('([^a-zA-Z]|^)usa( )*eu(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' swissusa ') 
#        regexp = re.compile('([^a-zA-Z]|^)how long(?=[^a-zA-Z]|$)')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' howlong ') 
        
#        regexp = re.compile('([^a-zA-Z]|^)customer support (services|service)(?=[^a-zA-Z]|$)')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' custsupserv ') 

#        regexp = re.compile('([^a-zA-Z]|^)payment processor(?=[^a-zA-Z]|$)')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' paymentprocessor ')  
        
        regexp = re.compile('([^a-zA-Z]|^)third[\- ]{0,1}(parties|party)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' thirdparti ')
        regexp = re.compile('([^a-zA-Z]|^)sub[\- ]{0,1}(processor|processors)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' subprocessor ')
        regexp = re.compile('([^a-zA-Z]|^)sub[\- ]{0,1}(contractor|contractors)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' subcontractor ')
        df_temp.sentence = df_temp.sentence.apply(remove_punct)       
        
        regexp = '([^a-zA-Z]|^)contact us(?=[^a-zA-Z]|$)'
        df_temp.sentence = [sentence if not bool(re.search(regexp, sentence)) else '' for sentence in df_temp.sentence ]
        
        regexp = re.compile('([^a-zA-Z]|^)privacy (policy|policies)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' pp ')
        regexp = re.compile('([^a-zA-Z]|^)standard contractual (clauses|clause)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' scc ')
        regexp = re.compile('([^a-zA-Z]|^)binding corporate (rules|rule)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' bcr ')
#        regexp = re.compile('([^a-zA-Z]|^)european data protection laws(?=[^a-zA-Z]|$)')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' edpl ')
        
#        regexp = re.compile('([^a-zA-Z]|^)(outside) (Agreement|Addendum|AGREEMENT|ADDENDUM)(?=[^a-zA-Z]|$)')
        
        regexp = re.compile('([^a-zA-Z]|^)data processing (agreement|addendum)(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' dpa ')
        regexp = re.compile('([^a-zA-Z]|^)(this|our) dpa(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' dpad ')
        regexp = re.compile('([^a-zA-Z]|^)amazon web services(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' aw ')
        regexp = re.compile('([^a-zA-Z]|^)google cloud(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' gcp ')
        
        df_temp.sentence = df_temp.sentence.str.split()
        df_temp.sentence = [' '.join(stem(sentence)) for sentence in df_temp.sentence]
                
#        regexp = re.compile('([^a-zA-Z]|^)not transfer(?=[^a-zA-Z])')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' ')
        
        regexp = re.compile('([^a-zA-Z]|^)(outsid (the|of the) (eu|eea|european union|european econom area))(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' outsideeu ')
        
        regexp = re.compile('([^a-zA-Z]|^)(outsid ((your|of your) (countri|territori)|(the|of the) ((countri|territori) where you live)))(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' outsidecountri ')
        regexp = re.compile('([^a-zA-Z]|^)countri other than the one in which you live(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' outsidecountri ')
        regexp = re.compile('([^a-zA-Z]|^)countri other than the one in which you live(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' outsidecountri ')
        regexp = re.compile('([^a-zA-Z]|^)other countri(?=[^a-zA-Z]|$)')
        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' outsidecountri ')
        
#        regexp = re.compile('([^a-zA-Z]|^)other countri(?=[^a-zA-Z]|$)')
#        df_temp.sentence = df_temp.sentence.str.replace(regexp, ' othercountri ')


        
        df_temp.sentence = df_temp.sentence.str.split()
                
        
        
        
        df_list.append(df_temp)
        

    df = pd.concat(df_list)
    df_sentences = pd.concat(df_list_full_sentences)

    return(df, df_sentences, df_list, df_list_full_sentences)


def get_countries(answer_list, df, n_countries, countries, question_id,nationalities=False, df_full=[]):
    ''' Renvoie moins de n pays à partir d'une configuration de:
        - La configuration de réponse: answer_list
        - Les phrases du text contenues dans le dataframe df '''
    
        
    if question_id in c.question_negative_key_words:
        labels = [(any(all(any(key_word in sentence for key_word in key_word_list)
                          for key_word_list in answer) for answer in answer_list) and all(key_word not in sentence for key_word in c.question_negative_key_words[question_id])) for sentence in df.sentence]
    else:
        labels = [any(all(any(key_word in sentence for key_word in key_word_list)
                          for key_word_list in answer) for answer in answer_list) for sentence in df.sentence]

    df_extract = df[labels]
    df_full_extract = df_full[labels]
#    if len(df_full) > 0:
#        df_full_extract = df_full[labels]
    country_extract = [[word for word in sentence if (word in countries or word in c.nationalities_dict)]
                       for sentence in df_extract.sentence]
    country_extract = [[c.nationalities_dict[word] if (word in c.nationalities_dict) else word for word in sentence]
                       for sentence in country_extract]
#    country_extract.extend([[c.nationalities_dict[word] for word in sentence if word in c.nationalities_dict]
#                   for sentence in df_extract.sentence if not 'languag' in sentence])
    if question_id in [18,11,9,5] and len(country_extract)>0:
        lengths = [len(set(countries)) for countries in country_extract if len(set(countries))<=n_countries]
        if lengths:
            max_countries = max(lengths)
            answer_country = list(set([countries for countries in country_extract if len(set(countries)) == max_countries][0]))
            index = [i for i in range(len(country_extract)) if len(set(country_extract[i])) == max_countries][0]
            answer_country = list(set(country_extract[index]))
            answer_country_justif = df_full_extract.sentence.iloc[index]
        else:
            answer_country = []
            answer_country_justif = ''

    else:
        answer_country = list(set(itertools.chain.from_iterable(country_extract)))
        answer_country_justif = ''
    codes = [c.df_countries.loc[c.df_countries.name == country, 'id'].iloc[0]
             for country in answer_country]
    codes.sort()
    country_codes = [0] * n_countries
    for i in range(min(len(codes), n_countries)):
        country_codes[i] = codes[i]
    if len(df_full) > 0:
        return(answer_country, list(df_full_extract.sentence), country_codes, answer_country_justif)
    else:
        return(answer_country, None, country_codes, answer_country_justif)


def regexp_pred_countries(df_list, df_list_full_sentences):
    #TODO back to one return
    res = [[] for i in range(len(df_list))]
    res_justifs = [[] for i in range(len(df_list))]
    for question_id in c.country_question_key_words:
        question_args = c.country_question_arguments[question_id]
        for df_i in range(len(df_list)):
            question_args['df'] = df_list[df_i]
            question_args['df_full'] = df_list_full_sentences[df_i]
            question_args['question_id'] = question_id
            answer_countries, full_sentences, country_codes, answer_country_justif = get_countries(
                **question_args)
            justifs = [answer_country_justif]*question_args['n_countries']
            res[df_i].extend(country_codes)
            res_justifs[df_i].extend(justifs)
    return(np.array(res).T, np.array(res_justifs).T)


def regexp_pred(df_list, df_list_full_sentences=None):
    question_key_words = c.question_key_words

    # Listing question ids
    questions = list(question_key_words)
    questions.sort()
    questions = [q for q in questions if q <= 22]

    estimates = []
    for question_id in question_key_words:
        answer_list = question_key_words[question_id]
        if question_id in c.question_negative_key_words:        
            answers = [any((any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer)
                   for answer in answer_list) and all(key_word not in sentence for key_word in c.question_negative_key_words[question_id]))
                    for sentence in df.sentence) for df in df_list]
        else:
            answers = [any(any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer)
                               for answer in answer_list) for sentence in df.sentence) for df in df_list]
        estimates.append(answers)

    estimates = np.array(estimates)
    estimates = estimates.astype(int)

    # Cas échéant de la question 22
    estimates[-2] = estimates[-1] + estimates[-2]
    estimates = estimates[:-1]
    for question_id in c.questions_inverses:
        row = c.boolean_questions.index(question_id)
        estimates[row] = 1 - estimates[row]

    return(estimates, question_key_words)

def regexp_pred_justif(df_list, df_list_full_sentences=None):
    question_key_words = c.question_key_words

    # Listing question ids
    questions = list(question_key_words)
    questions.sort()
    questions = [q for q in questions if q <= 22]

    estimates = []
    answers_justif = []
    for question_id in question_key_words:
        answer_list = question_key_words[question_id]
        answers = []
        answers_justif_i = []
        for df_i in range(len(df_list)):
            df = df_list[df_i]
            df_full = df_list_full_sentences[df_i]
            for sentence_i in range(len(df.sentence)):
                sentence = df.sentence.iloc[sentence_i]
                if question_id in c.question_negative_key_words:
                    resp = (any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer)
                       for answer in answer_list) and all(key_word not in sentence for key_word in c.question_negative_key_words[question_id]))
                else:
                    resp = any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer) for answer in answer_list)
                if resp:
                    break
            answers.append(resp)
            if question_id != 23:
                if resp:
                    answers_justif_i.append(df_full.sentence[sentence_i])
                else:
                    answers_justif_i.append([''])
            else:
                if resp:
                    answers_justif[11][df_i] = df_full.sentence[sentence_i]

        answers_justif.append(answers_justif_i)
        estimates.append(answers)

    estimates = np.array(estimates)
    estimates = estimates.astype(int)

    # Cas échéant de la question 22
    estimates[-2] = estimates[-1] + estimates[-2]
    estimates = estimates[:-1]
    for question_id in c.questions_inverses:
        row = c.boolean_questions.index(question_id)
        estimates[row] = 1 - estimates[row]
    
    answers_justif.pop()
    return(estimates, question_key_words, answers_justif)


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
    estimates, question_key_words,answers_justif = regexp_pred_justif(df_list, df_list_full_sentences)
    res, res_justifs = regexp_pred_countries(df_list, df_list_full_sentences)

    train_df = pd.read_csv('resources/train.csv')
    train_df['question_number_aux'] = train_df.question_number.mod(22)
    train_df.loc[train_df['question_number_aux']
                 == 0, 'question_number_aux'] = 22
    
    replace_dict = {'Yes': 1,
                    'No': 0,
                    'Yes, mentioned only': 1,
                    'Yes, and precise durations are specified':2,
                    'Not mentionned': 0}
    columns = c.boolean_questions
    targets_2 = pd.read_excel('C:/Users/adnane/Desktop/train2.xlsx')
    targets_2['Nom du fournisseur'] = targets_2['Nom du fournisseur'].str.lower()
    targets_2 = targets_2.sort_values('Nom du fournisseur')
    targets_2 = targets_2.replace(replace_dict)
    targets = targets_2[columns].to_numpy().T
    
#    targets = []
#    for question_id in c.boolean_questions:
#        if question_id <= 22:
#            answer_list = list(
#                train_df[train_df['question_number_aux'] == question_id].response_id)
#            targets.append(answer_list)
#    targets = np.array(targets)

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
    

    if question_id in c.question_negative_key_words: 
        labels = [(any(all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer)
                   for answer in answer_list) and all(key_word not in sentence for key_word in c.question_negative_key_words[question_id]))
                    for sentence in df.sentence]
    else:
        labels = [any(all(any(key_word in sentence for key_word in key_word_list)
                      for key_word_list in answer) for answer in answer_list) for sentence in df.sentence]
    x = df[labels]
    y = df_sentences[labels]

    question_num = c.boolean_questions.index(question_id)
    documents = np.where(
        (targets[question_num] - estimates[question_num]) != 0)[0] + 1

    print('Documents avec faute', [paths[d - 1] for d in documents])
    
    x_fault = x[x.path.isin([paths[d - 1] for d in documents])]
    y_fault = y[y.path.isin([paths[d - 1] for d in documents])]
    
    print(estimates[question_num])
    print(targets[question_num])

    # =============================================================================
    # Pays
    # =============================================================================

    question_id = 11
#    for question_id in c.country_question_arguments:
    question_args = c.country_question_arguments[question_id]
    results_countries = {}
    results_sentences = {}
    for df_i in range(len(df_list)):
        name = path_to_name(df_list[df_i].iloc[0].path)
        question_args['df'] = df_list[df_i]
        question_args['df_full'] = df_list_full_sentences[df_i]
        answer_countries, full_sentences, country_codes, answer_country_justif = get_countries(**question_args)
        results_countries[name] = answer_countries
        results_sentences[name] = list(full_sentences)
    
        question_args['answer_list']

    
#    sentences = [['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']]
#    sentence = ['at', 'docusign', 'privaci', 'is', 'a', 'prioriti']
#    labels = [all(any(key_word in sentence for key_word in key_word_list) for key_word_list in answer) for answer in answer_list]
#    x = df[labels]
