import os
from typing import List, Dict

from datathon_ai.form_company_filling import FormCompanyFilling
from datathon_ai.extractors import BasicCountryExtractor, BasicExtractor
from datathon_ai.interfaces import FormDataModel, CountryReferential, COUNTRY_QUESTIONS_NUMBERS, \
    NOT_COUNTRY_QUESTIONS_NUMBERS

from doc_to_sentences import text_to_sentences
from qa_bool_regexp import *
import config as c


def main() -> Dict[int, int]:
    """
    USED BY DATACHALLENGE PLATFORM.
    Function that makes predictions. The .txt documents are located in the /data folder at the root of your code.
    :return: a dictionary with question_number as keys and answer_id as values.
    If number of keys in dictionary is not equaled to number_company * nb_question_by_company, it raises an
    error.
    """
    # DOCUMENTS DIRECTORY
    # Path of the directory that contains the .txt documents. One .txt document by company. IT NEEDS TO BE "/data" when you upload it in data challenge platform. For test in local, you can modifiy to match your data path.
    documents_directory = "/data"
    path_to_files: List[str] = [os.path.join(
        documents_directory, file) for file in os.listdir(documents_directory)]
    assert len(path_to_files) == 10  # 10 files in documents directory
    # Sort list of path file by alphabetical order to match ground truth annotations order : IT IS ESSENTIAL.
    path_to_files.sort()

    # INITIALIZATION OF YOUR OBJECTS
    data_model = FormDataModel.from_json_file(
        os.path.join(os.path.dirname(__file__), "resources", "data-model.json")
    )
    country_referential = CountryReferential.from_csv(
        os.path.join(os.path.dirname(__file__),
                     "resources", "countries_code.csv")
    )
    form_company_filling = FormCompanyFilling([
        BasicExtractor(
            question_ids=NOT_COUNTRY_QUESTIONS_NUMBERS,
            form_data_model=data_model
        ),
        BasicCountryExtractor(
            question_ids=COUNTRY_QUESTIONS_NUMBERS,
            form_data_model=data_model,
            country_code_referential=country_referential
        )
    ])

    # COMPUTE PREDICTION BY FILE (ie company)
    # print("##################################")
    # print("RUNNING PREDICTION")
    results: Dict[int, int] = {}

    res_dict = text_to_sentences(path_to_files)
    df, df_sentences, df_list, df_list_full_sentences = pre_processing(
        res_dict, path_to_files)
    estimates, question_key_words, answers_justif = regexp_pred_justif(
        df_list, df_list_full_sentences)
    country_estimates, country_justifs = regexp_pred_countries(
        df_list, df_list_full_sentences)

    estimates = estimates.T
    country_estimates = country_estimates.T
    country_justifs = country_justifs.T
    answers_justif = answers_justif.T

    for i, path in enumerate(path_to_files):
        print(f"File : {path}")
        # with open(path, "r") as input_file:
        #     text = input_file.read()

        estimates_i = estimates[i]
        country_estimates_i = country_estimates[i]
        answers = {c.boolean_questions[i]: estimates_i[i]
                   for i in range(len(c.boolean_questions))}
        answers_countries = {c.country_questions[i]: country_estimates_i[i]
                             for i in range(len(c.country_questions))}
        answers.update(answers_countries)

        justif_i = answers_justif[i]
        country_justifs_i = country_justifs[i]
        justifs = {c.boolean_questions[i]: justif_i[i]
                   for i in range(len(c.boolean_questions))}
        justifs_countries = {c.country_questions[i]: country_justifs_i[i]
                             for i in range(len(c.country_questions))}
        justifs.update(justifs_countries)
        form_company_response = form_company_filling.fill((answers, justifs))
        # ESSENTIAL : Sort the response by question number for each company
        form_company_response.sort_by_question_id()
        for answer in form_company_response.answers:
            # ESSENTIAL : each company has 22 questions. Each question_number in results should be unique
            question_number = answer.question_id + i * 22
            results[question_number] = answer.answer_id

    # CHECK FORMAT RESULTS IS DATACHALLENGE PLATFORM COMPATIBLE
    assert len(results) == len(path_to_files) * \
        (len(COUNTRY_QUESTIONS_NUMBERS) + len(NOT_COUNTRY_QUESTIONS_NUMBERS))
    assert set(list(results.keys())) == {i for i in range(1, 221)}
    return results


if __name__ == "__main__":
    main()
