#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:42:55 2020

@author: jores
"""

"""
Created on Mon Nov 30 22:42:55 2020

@author: jores
"""
import glob
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
from doc_to_sentences import text_to_sentences
 
def load_model(module_url) :
    import time;
    st = time.time()
    model = hub.load(module_url)
    elapsed_time = time.time() - st
    print ('Temps de chargement du modèle', round(elapsed_time/60, 2))
    return model

def embed(input):
  return model(input)

def load_question_answer(path_question) :

    questions = pd.read_excel(path_question)
    answers = pd.read_excel(path_question, sheet_name=1)
    answers['Nom du fournisseur'] = answers['Nom du fournisseur'].apply(lambda x : ''.join(x.lower().split()))
    questions['Question id'] = questions['Question id'].apply(lambda x : ''.join(x.lower().split()))
    answers.columns = [str(elt) for elt in answers.columns]
    return questions, answers
 

def get_similarities(dico_text, answers, questions, model, top_similarities = 10) :
    """
    Extracting the {top_similarities} similar sentences given a question and return 
    a dataframe including these sentences for each couple (supplier, question) 
    """
    dict_result = {'supplier' : [],
                   'num_question': [],
                   'question': [],
                   'top_paragraph' : [],
                   'similarity': []}
    
    dict_analysis = {'supplier' : [],
                   'num_question': [],
                   'question': [],
                   'similarity': [],
                   'nb_after':[]}
    
    for supplier, text in dico_text.items() :
        supplier = supplier.split('/')[-1][:-4]
        paragraph_emb = embed(text) ## vectorisation of the sentences #
        print(f"Suppliers {supplier}")
        
        for num_question in questions['Question id'].unique() :
            try :
                answer, extrait = answers.loc[answers['Nom du fournisseur']== supplier][[num_question, 
                                              'Extrait' + num_question]].to_records(index=False)[0]
            except :
                answer = 'No'
                extrait = "abcde1234"
            try :
                yolo = np.isnan(extrait) 
                extrait = "abcde1234"
            except :
                pass
            question_0 = questions.loc[questions['Question id'] == num_question]['Questions'].iloc[0]
            index_extrait_in_text = np.nan
            
            ## finding the position of the optimal paragraph related to the question (according to experts) in the text
            for i, elt in enumerate(text) :
                if extrait.lower().strip() in elt.lower().strip() :
                    index_extrait_in_text = i
                    break       
            question_emb = embed([question_0])
            
            ######## similarities computations ##########
            
            p1 = tf.nn.l2_normalize(paragraph_emb, axis=1)
            q1 = tf.nn.l2_normalize(question_emb, axis=1)
            cosine_similarities = tf.reduce_sum(tf.multiply(p1, q1), axis=1)
            clip_cosine_similarities = tf.clip_by_value(cosine_similarities, -1.0, 1.0)
            scores = 1.0 - tf.acos(clip_cosine_similarities).numpy() / np.pi
            try :
                score_extrait = scores[index_extrait_in_text]
            except :
                score_extrait = 0
            
            nb_after = len(np.where(scores > score_extrait)[0]) ## nb of sentences whichs similarity is higher than the optimal paragraph
            text_interessants = list(np.array(text)[np.argsort(scores)[-top_similarities:]]) ## these sentences
            sim_scores = list(scores[np.argsort(scores)[-top_similarities:]]) ## the related scores
            
            dict_result['top_paragraph'].extend(text_interessants)
            dict_result['similarity'].extend(sim_scores)
            dict_result['num_question'].extend([num_question]*top_similarities)
            dict_result['question'].extend([question_0]*top_similarities)
            dict_result['supplier'].extend([supplier]*top_similarities)
            
            dict_analysis['num_question'].extend([num_question])
            dict_analysis['question'].extend([question_0])
            dict_analysis['supplier'].extend([supplier])         
            dict_analysis['similarity'].extend([score_extrait])
            dict_analysis['nb_after'].extend([nb_after/len(text)])
            print(f"Question {num_question} : similarité extrait/question = {score_extrait}")
            print(f"Nombre de paragraphes de similarité plus importante : {len(np.where(scores > score_extrait)[0])} ")
            print("")

    df = pd.DataFrame.from_dict(dict_result)
    df_perf = pd.DataFrame.from_dict(dict_analysis)
    return df, df_perf

if __name__ == '__main__' :
    folder = 'data'
    path_question = 'annotations_example_dataset.xlsx'
    filenames = os.listdir(folder)
    paths = [os.path.join(folder, filename) for filename in filenames]
    dico_text = text_to_sentences(paths)
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    
    model = load_model(module_url)
    questions, answers = load_question_answer(path_question)
    df, df_perf = get_similarities(dico_text, answers, questions, model, top_similarities = 10)
