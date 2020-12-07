# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:51:29 2020

@author: adnane
"""
import pandas as pd
from utils import stem

# dataframe des nationalité -> pays
nationalities = pd.read_csv('resources/nationalities.txt')

boolean_questions = [1, 2, 3, 4, 8, 13, 14, 15, 16, 17, 21, 22]
country_questions = [x for x in range(1, 23) if not x in boolean_questions]

# Questions dont on cherche les mots clés de la négatif
questions_inverses = [4]

# liste de pays de l'eea
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
                'Norway',
                'Monaco',
                'uk']


eu_countries = [country.lower() for country in eu_countries]

# Chargement de tous les pays + processing sur pays et nationalités
df_countries = pd.read_csv('resources/countries_code.csv')
df_countries.name = df_countries.name.str.lower()
df_countries.alpha2 = df_countries.alpha2.str.lower()
df_countries.alpha3 = df_countries.alpha3.str.lower()
country_list = list(df_countries.name)
country_list.remove('jersey')  # Remove problematic countries
country_list.append('usa')
country_list.append('uk')
nationalities.loc[max(nationalities.index) + 1] = ['english', 'uk']

nationality_country_replace_dict = {
    'United States': 'usa',
    'United Kingdom': 'uk'}

nationalities.country = nationalities.country.replace(
    nationality_country_replace_dict)
nationalities.country = nationalities.country.str.lower().str.strip()
nationalities.nationality = nationalities.nationality.str.lower().str.strip()

nationalities = nationalities[nationalities.country.isin(country_list)]
nationalities = nationalities[~nationalities.nationality.isin(
    ['us', 'u.s.', 'uk'])]
nationalities_list = list(nationalities.nationality)
nationalities = nationalities.set_index('nationality')
nationalities.country = stem(nationalities.country)
nationalities_dict = nationalities.to_dict()['country']

country_replace_dict = {
    'united states': 'usa',
    'united kingdom': 'uk'}
df_countries.name = df_countries.name.replace(country_replace_dict)
df_countries.name = stem(df_countries.name)


non_eu_countries = [
    country for country in country_list if country not in eu_countries]

country_list = stem(country_list)
non_eu_countries = stem(non_eu_countries)
eu_countries = stem(eu_countries)

# Mots clés interdits dans les réponses
question_negative_key_words = {
    4: ['pp'],
    5: ['embargo']

}

# Mots clés ciblés pour les questions booléennes, on peut avoir plusieurs structures de réponse par question
question_key_words = {
    1: [[['personal'], ['data', 'information']]],
    2: [
        [['dpad']]
    ],
    3: [
        [['data', 'information'], ['transfer', 'forward', 'access',
                                   'disclosed', 'share'], ['outsideeu', 'outsidecountri']],
        [['hosted'], non_eu_countries]
    ],
    4: [
        [['transfer', 'forward', 'access', 'disclosed', 'share'], [
            'data', 'information'], ['outsidecountri', 'outsideeu']]
    ],
    8: [[['bcr', 'scc']]],
    13: [[['iso27001']],
         [['iso', '27001']]],
    14: [[['payment', 'price']]],
    15: [[['transfer', 'forward', 'access', 'disclosed', 'share'], ['data', 'information'], ['thirdparties', 'subcontractors', 'subprocessors', 'parties', 'contractors']]],
    16: [
        [['crm', 'monser', 'appmon', 'errtrac', 'marketautomation', 'businessanalytics', 'imagehosting', 'customerengagement',
          'digitalsignature', 'conversationrecording', 'datawarehouse', 'cloudserviceprovid', 'sitesearch', 'supportsystem', 'eventticketing', 'datavisualization',
          'intelligentsearchtechnology', 'intelligentanalytics', 'authenticationsystems', 'billcollection',
          'chatservices', 'helpdeskservices', 'systemadministrationservices', 'exceptionreporting', 'customerrelationshipmanagement', 'subscriptionmanagement']],
    ],
    17: [[['thirdparties', 'subcontractors', 'subprocessors', 'parties', 'contractors'], ['listed']],
         ],
    21: [[['audit'], ['right', 'allow', 'permit', 'agree']]],
    22: [[['data', 'information'], ['retention', 'retain']],
         [['data', 'information'], ['delete'], ['end']]],
    23: [[['data', 'information'], ['retention', 'retain'], ['days', 'months', 'years', 'weeks']]],
}

# stemming des mots clés
for question_id in question_key_words:
    answers= question_key_words[question_id]
    answers= [[stem(keyword_list) for keyword_list in answer]
               for answer in answers]

    question_key_words[question_id]= answers


# Mots clés ciblés pour les questions pays, on peut avoir plusieurs structures de réponse par question
country_question_key_words= {
    5: [[['data', 'information'], ['transfer'], [country for country in non_eu_countries]],
        [['hosting'], [country for country in non_eu_countries]]
        ],

    9: [[['arbitration', 'jurisdiction', 'courts'], country_list + nationalities_list]],
    11: [[['arbitration', 'jurisdiction', 'courts'], country_list + nationalities_list]],
    18: [
        [['subprocessors', 'serviceprovider'], [
            'location', 'country', 'address', 'where']]
    ],
}

# stemming des mots clés
for question_id in country_question_key_words:
    answers= country_question_key_words[question_id]
    answers= [[stem(keyword_list) for keyword_list in answer]
               for answer in answers]
    country_question_key_words[question_id]= answers

# Varier le nombre de pays an réponse, les pays ciblés et la recherche ou non de nationalité pour chaque question
country_question_arguments= {
    5: {'n_countries': 3, 'countries': non_eu_countries},
    9: {'n_countries': 2, 'countries': country_list, 'nationalities': True},
    11: {'n_countries': 2, 'countries': country_list, 'nationalities': True},
    18: {'n_countries': 3, 'countries': country_list}
}

# On ajoute les mots clés aux paramètres
for question_key in country_question_arguments:
    country_question_arguments[question_key]['answer_list']= country_question_key_words[question_key]


print('Config file loaded')
