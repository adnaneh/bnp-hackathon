# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:51:29 2020

@author: adnane
"""
import pandas as pd
from utils import stem

print ('test')

stem('usa or other countries'.split())
#outside your territory
#outside your country
#outside of your country
#stem('outside of the country where you live'.split())
#outside the country where you live

#sentence = ['10', 'list', 'of', 'sub', 'processor', 'aircal', 'will', 'ensur', 'that', 'a', 'suitabl', 'data', 'transfer', 'mechan', 'is', 'in', 'place', 'for', 'ani', 'subprocessor', 'who', 'process', 'european', 'person', 'data', 'outsideeu', 'or', 'where', 'the', 'client', 'is', 'subject', 'to', 'data', 'protect', 'act', '2018', 'for', 'it', 'process', 'the', 'uk']
#all(key_word not in sentence for key_word in c.question_negative_key_words[4])

' '.join(stem('error tracking'.split()))

nationalities = pd.read_csv('resources/nationalities.txt')

# For now 22 is set as boolean but needs to be tweaked
boolean_questions = [1,2,3,4,8,13,14,15,16,17,21,22]
country_questions = [x  for x in range(1,23) if not x in boolean_questions]

questions_inverses = [4]

doc_to_id_map = {'docusign': 0,
                 'hotjar': 1,
                 'iadvize': 2,
                 'mailjet': 3,
                 'marvelapp': 4,
                 'postman': 5,
                 'slack': 6,
                 'typeform': 7,
                 'wordpress': 8,
                 'zoom': 9}

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



df_countries = pd.read_csv('resources/countries_code.csv')
df_countries.name = df_countries.name.str.lower()
df_countries.alpha2 = df_countries.alpha2.str.lower()
df_countries.alpha3 = df_countries.alpha3.str.lower()
country_list = list(df_countries.name) 
country_list.remove('jersey') #Remove problematic countries
country_list.append('usa')
country_list.append('uk')
nationalities.loc[max(nationalities.index)+1] = ['english','uk']

nationality_country_replace_dict = {
        'United States' : 'usa',
        'United Kingdom': 'uk'}

nationalities.country = nationalities.country.replace(nationality_country_replace_dict)
nationalities.country= nationalities.country.str.lower().str.strip()
nationalities.nationality= nationalities.nationality.str.lower().str.strip()

nationalities = nationalities[nationalities.country.isin(country_list)]
nationalities = nationalities[~nationalities.nationality.isin(['us','u.s.','uk'])]
nationalities_list = list(nationalities.nationality)
nationalities = nationalities.set_index('nationality')
nationalities.country = stem(nationalities.country)
nationalities_dict = nationalities.to_dict()['country']

country_replace_dict = {
        'united states' : 'usa',
        'united kingdom': 'uk'}
df_countries.name = df_countries.name.replace(country_replace_dict)
df_countries.name = stem(df_countries.name)
#country_list = list(df_countries.name) + \
#    list(df_countries.alpha2) + list(df_countries.alpha3) 
    
non_eu_countries = [country for country in country_list if country not in eu_countries]

country_list = stem(country_list)
non_eu_countries = stem(non_eu_countries)
eu_countries = stem(eu_countries)


question_negative_key_words = {
#        4 : ['thirdparti', 'affili', 'dpa', 'dpad', 'sda', 'edpl', 'subprocessor', 'pp']
#        4 : ['dpa', 'dpad', 'sda', 'edpl', 'pp'],
        4 : ['pp'],
        5 : ['embargo']


        }

question_key_words = {
    1: [[['personal'], ['data','information']]],
    2: [
#        [['data'], ['processing'], ['agreement','addendum']],
        [['dpad']]
        ],
    3: [
        [['data','information'],['transfer', 'forward','access','disclosed','share'], ['outsideeu', 'outsidecountri']],
#        [['transfer', 'access'], ['other'],['countries']],
#        [['transfer', 'access'], ['outside'], ['eu', 'european', 'eea']],
#        [['data','information'],['transfer', 'access'], non_eu_countries],
        [['hosted'],non_eu_countries]
        ],
    4: [
#        [['data','information'],['transfer'], ['outsideeu', 'outsidecountri']],
#        [['data','information'],['transfer'], country_list]
#        [['data','information'],['transfer'],['outsidecountri']]
#        [['transfer'],['information'], non_eu_countries],
#        [['transfer'],['data'], [country for country in country_list if country!='usa']]
        [['transfer', 'forward','access','disclosed','share'],['data','information'], ['outsidecountri', 'outsideeu']]

        

#        [['data'],['transfer', 'access'], ['other'], ['country']],
#        [['data'],['transfer', 'access'], ['outside']],
#        [['gcp','aw']]
        ],
    8: [[['bcr', 'scc']]],   
    13: [[['iso27001']],
         [['iso', '27001']]], #TODO include the name of the software in the sentence
    14: [[['payment','price']]],
    15: [[['transfer', 'forward','access','disclosed','share'],['data','information'],['thirdparties','subcontractors','subprocessors','parties','contractors']]],
#    16: [[['cloud'],['service'],['provider']],
#         [['monitoring'], ['services']],
#         [['application'] ,['monitoring']],
#         [['error'],['tracking']],
#         [['payment'] ,['processor']],
#         [['marketing'], ['automation'], ['software']],
#         [['business'],['analytics']],
#         [['crm']],
#         [['set','below'],['parties']]
#         ],
    16: [
         [['crm','monser','appmon','errtrac','marketautomation', 'businessanalytics', 'imagehosting', 'customerengagement',
           'digitalsignature', 'conversationrecording', 'datawarehouse', 'cloudserviceprovid', 'sitesearch', 'supportsystem', 'eventticketing', 'datavisualization',
           'intelligentsearchtechnology', 'intelligentanalytics', 'authenticationsystems', 'billcollection',
           'chatservices', 'helpdeskservices', 'systemadministrationservices','exceptionreporting','customerrelationshipmanagement', 'subscriptionmanagement']],
#         [['thirdparties','contractors','parties'],['transfer', 'forward','access','disclosed','share'], ['purposes'],['table']],
        ],
    17: [[['thirdparties','subcontractors','subprocessors','parties','contractors'], ['listed']],
         ],
    21: [[['audit'],['right','allow','permit','agree']]],
    22: [[['data','information'], ['retention','retain']],
         [['data','information'], ['delete'],['end']],
#         [['data','information'], ['delete'],['days', 'months', 'years', 'weeks']],
#         [['data','information'],['days', 'months', 'years', 'weeks']]
         ], #TODO complete in details
    # cas échéant de la question 22
    23: [
#        [['data','information'],['days', 'months', 'years', 'weeks']],
        [['data','information'], ['retention','retain'],['days', 'months', 'years', 'weeks']]
    ],
    
    # Country questions
#        5 : {[['data','information'],['transfer', 'access'], c.non_eu_countries],
#        [['data','information'],['transfer', 'access'], ['united'],['states']]}
}

for question_id in question_key_words:
    answers = question_key_words[question_id]
    answers = [[stem(keyword_list) for keyword_list in answer] for answer in answers]

    question_key_words[question_id] = answers
    


liens_questions_pays = {
        4: [5,6,7],
        8: [9,10,11,12],
        17: [18,19,20]
        }

country_question_key_words = {
        5: [[['data','information'],['transfer'], [country for country in non_eu_countries]],
            [['hosting'], [country for country in non_eu_countries]]
        ],
#        9: [[['law'], country_list+nationalities_list]],
#        11: [[['arbitration','jurisdiction','courts'],country_list+nationalities_list]],
        9: [[['arbitration','jurisdiction','courts'],country_list+nationalities_list]],
        11: [[['arbitration','jurisdiction','courts'],country_list+nationalities_list]],
#        18: [[['arbitration','jurisdiction'],country_list]]
        18:[
            [['subprocessors','serviceprovider'],['location','country','address','where']]
#            [['subprocessors','affiliates'],['location','country','address','where']]
            ],
#            [['affiliates'],['location','country', 'address', 'where']]]
        }

for question_id in country_question_key_words:
    answers = country_question_key_words[question_id]
    answers = [[stem(keyword_list) for keyword_list in answer] for answer in answers]
    country_question_key_words[question_id] = answers

country_question_arguments = {
        5: {'n_countries':3, 'countries':non_eu_countries},
        9: {'n_countries':2, 'countries':country_list, 'nationalities': True},
        11: {'n_countries':2, 'countries':country_list, 'nationalities': True},
        18: {'n_countries':3, 'countries':country_list}
        }

for question_key in country_question_arguments:
    country_question_arguments[question_key]['answer_list'] = country_question_key_words[question_key]

    
    
print('Config file loaded')
