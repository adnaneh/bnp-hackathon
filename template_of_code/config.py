# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:51:29 2020

@author: adnane
"""
import pandas as pd
# For now 22 is set as boolean but needs to be tweaked
boolean_questions = [1,2,3,4,8,13,14,15,16,17,21,22]

country_questions = [x  for x in range(1,23) if not x in boolean_questions]

eu_countries = ['Austria',
                 'Belgium',
                 'Bulgaria',
                 'Croatia',
                 'Cyprus',
                 'Czech',
                 'Denmark',
                 'Estonia',
                 'Finland',
                 'France',
                 'Germany',
                 'Greece',
                 'Hungary',
                 'Ireland',
                 'Italy',
                 'Latvia',
                 'Lithuania',
                 'Luxembourg',
                 'Malta',
                 'Netherlands',
                 'Poland',
                 'Portugal',
                 'Romania',
                 'Slovakia',
                 'Slovenia',
                 'Spain',
                 'Sweden',
                 'Switzerland',
                 'Iceland',
                 'Liechtenstein',
                 'Norway']

eu_countries = [country.lower() for country in eu_countries]

df_countries = pd.read_csv('resources/countries_code.csv')
df_countries.name = df_countries.name.str.lower()
df_countries.alpha2 = df_countries.name.str.lower()
df_countries.alpha3 = df_countries.name.str.lower()
country_list = list(df_countries.name) + \
    list(df_countries.alpha2) + list(df_countries.alpha3)
    
non_eu_countries = [country for country in country_list if country not in eu_countries]
