from typing import List

from datathon_ai.interfaces import FormDataModel, QuestionResponse, COUNTRY_QUESTIONS_NUMBERS, CountryReferential
from .question_extractor import QuestionExtractor
from .utils import get_dico_dummy_answers


class BasicCountryExtractor(QuestionExtractor):
    def __init__(self, question_ids: List[int], form_data_model: FormDataModel,
                 country_code_referential: CountryReferential):
        for q_number in question_ids:
            assert q_number in COUNTRY_QUESTIONS_NUMBERS
        super().__init__(question_ids, form_data_model)
        self.country_code_referential = country_code_referential

    def extract(self, text: str) -> List[QuestionResponse]:
        responses = []
        for question_id in self.question_ids:
            answer, question_id, justification = self.predict_regexp(
                text, question_id)
            responses.append(
                QuestionResponse(
                    answer_id=answer, question_id=question_id, justification=justification)
            )
        return responses

    def predict_regexp(self, text, question_id):
        return text[question_id], question_id, "YOLO"
