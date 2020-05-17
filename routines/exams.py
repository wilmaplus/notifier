#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON
from wilma_connector.wilma_client import WilmaClient


class Exams(AbstractRoutine):
    def __init__(self, push_utils):
        super().__init__("exams", push_utils)

    def check(self, wilmaserver, wilmasession, enc_pass, push_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        exams = wilma_client.getExams()
        if not exams.is_error():
            return exams.get_exception()
        offline_data_pt = self.get_file(enc_pass, push_id)
        if offline_data_pt is not None:
            offline_data = convertFromJSON(offline_data_pt)
            for l_exam in exams:
                found = False
                for o_exam in offline_data:
                    if o_exam['ExamId'] == l_exam['ExamId']:
                        found = True
                        break
                if not found:
                    # TODO send push
                    ...

        self.save_file(convertToJSON(exams), enc_pass, push_id)
        return None




