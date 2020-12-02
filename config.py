# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:51:29 2020

@author: adnane
"""

# For now 22 is set as boolean but needs to be tweaked
boolean_questions = [1,2,3,4,8,13,14,15,16,17,21,22]

country_questions = [x  for x in range(1,23) if not x in boolean_questions]


