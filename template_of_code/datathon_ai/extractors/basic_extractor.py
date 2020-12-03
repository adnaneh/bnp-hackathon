from typing import List

from datathon_ai.interfaces import FormDataModel, QuestionResponse
from .question_extractor import QuestionExtractor


class BasicExtractor(QuestionExtractor):
    def __init__(self, question_ids: List[int], form_data_model: FormDataModel):
        super().__init__(question_ids, form_data_model)

    def extract(self, text: str) -> List[QuestionResponse]:
        responses = []
        for question_id in self.question_ids:
            question_data_model = self.form_data_model.get_specific_question_data_model(question_id)
            available_answer = [answer.id_answer for answer in question_data_model.answers]
            answer = available_answer[0]
            justification = text[:10]
            responses.append(
                QuestionResponse(answer_id=answer, question_id=question_id, justification=justification)
            )
        return responses
    