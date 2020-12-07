from typing import List

from datathon_ai.interfaces import FormDataModel, QuestionResponse
from .question_extractor import QuestionExtractor


class BasicExtractor(QuestionExtractor):
    def __init__(self, question_ids: List[int], form_data_model: FormDataModel):
        super().__init__(question_ids, form_data_model)

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
        answers, justifs = text[0], text[1]
        return answers[question_id], question_id, justifs[question_id]
