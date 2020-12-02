# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 18:23:30 2020

@author: adnane
"""
import pandas as pd 
import numpy as np

train_df = pd.read_csv('resources/train.csv')
train_df['question_number_aux'] = train_df.question_number.mod(22)
train_df.loc[train_df['question_number_aux']==0,'question_number_aux'] = 22 

targets = []
for question_id in range(1,23):
    answer_list = list(train_df[train_df['question_number_aux'] == question_id].response_id)
    targets.append(answer_list)
targets = np.array(targets)

n_samples = targets.shape[1]
question_to_acc_map_baseline = {}
baseline = np.array([[np.bincount(x).argmax() for x in targets]] * targets.shape[1]).T
for row in range(targets.shape[0]):
    acc = 1 - np.count_nonzero(targets[row] - baseline[row])/n_samples
    question_to_acc_map_baseline[row+1] = acc

