#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 18:15:06 2020

@author: jores
"""

import pandas as pd
import numpy as np
import os

def get_dico_dummy_answers() :
    path = os.path.dirname(__file__).split('/')[:-2]
    path = '/'.join(path)
    path_train = path + '/resources/train.csv'
    train_df = pd.read_csv(path_train)
    train_df['question_number_aux'] = train_df.question_number.mod(22)
    train_df.loc[train_df['question_number_aux']==0,'question_number_aux'] = 22 
    
    targets = []
    for question_id in range(1,23):
        answer_list = list(train_df[train_df['question_number_aux'] == question_id].response_id)
        targets.append(answer_list)
    targets = np.array(targets)
    baseline = np.array([[np.bincount(x).argmax() for x in targets]] * targets.shape[1]).T
    dico = {question_id : baseline[question_id-1, 0] for question_id in range(1, 23)}
    return dico
    

