from typing import List

from datathon_ai.interfaces import QuestionResponse, FormDataModel


class QuestionExtractor:
    """
    A QuestionExtractor is a type of extractor that extracts the answers for a list of question ids.
    """

    def __init__(self, question_ids: List[int], form_data_model: FormDataModel):
        self.question_ids = question_ids
        self.form_data_model = form_data_model

    def extract(self, text) -> List[QuestionResponse]:
        raise NotImplementedError
