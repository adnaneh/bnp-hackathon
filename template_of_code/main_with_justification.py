import os
import sys
from typing import List

from datathon_ai.form_company_filling import FormCompanyFilling
from datathon_ai.extractors import BasicExtractor, BasicCountryExtractor
from datathon_ai.interfaces import FormDataModel, CountryReferential, COUNTRY_QUESTIONS_NUMBERS, \
    NOT_COUNTRY_QUESTIONS_NUMBERS

from doc_to_sentences import text_to_sentences
from qa_bool_regexp import *
import config as c


def main_with_justification(documents_directory: str, output_directory: str):
    """
    Function that makes predictions with justification.
    :param documents_directory: path of directory that contains the .txt documents. One .txt document by company.
    :param output_directory: path of directory where to dump the answers and justifications hy question.
    Dumped file is under .txt format and has the following structure for each .txt file in documents_directory.
    ### Company : docusign.txt ###
    Question <question_number> | Answer <answer_id> | Justification <justification>
    """
    # Initiation of your objects
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
        ),
    ])

    # Get path of files
    path_to_files: List[str] = [os.path.join(
        documents_directory, file) for file in os.listdir(documents_directory)]
    assert len(path_to_files) == 10  # 10 files in documents directory
    # Sort list of path file by alphabetical order to match ground truth annotations order.
    path_to_files.sort()

    # Init file in output_directory
    path_output_file = os.path.join(output_directory, "answers.txt")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Compute your prediction by file (ie company)
    output_txt = ""

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

    i = -1
    for path in path_to_files:
        i += 1
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

        print(f"Running predictions for file : {path}")
        output_txt += f"### Company : {os.path.basename(path)} ###\n"
#        with io.open(path, mode="r", encoding="utf-8") as input_file:
#            text = input_file.read()
        form_company_response = form_company_filling.fill((answers, justifs))
        # Sort the response by question number for each company
        form_company_response.sort_by_question_id()
        for answer in form_company_response.answers:
            output_txt += f"Question {answer.question_id} | Answer {answer.answer_id} | Justification {answer.justification}\n"
        output_txt += "\n\n"

    with open(path_output_file, "w") as output_file:
        output_file.write(output_txt)


if __name__ == "__main__":
    documents_directory = sys.argv[1]
    output_directory = sys.argv[2]
    main_with_justification(documents_directory, output_directory)
