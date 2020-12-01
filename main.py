#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:15:48 2020

@author: jores
"""

import numpy as np
import os
from doc_to_sentences import text_to_sentences
from filtering_with_embeddings import get_similarities, load_question_answer, load_model
from answering_questions import get_answers ## to do
from evaluate import evaluation ## to do

if __name__ == '__main__' :
    folder = 'data'
    path_question = 'Example_dataset_explained/annotations_example_dataset.xlsx'
    filenames = os.listdir(folder)
    paths = [os.path.join(folder, filename) for filename in filenames]
    dico_text = text_to_sentences(paths)
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    
    model = load_model(module_url)
    questions, answers = load_question_answer(path_question)
    df, df_perf = get_similarities(dico_text, answers, questions, model, top_similarities = 10)
    answers = get_answers(df)
    results = evaluation(answers)