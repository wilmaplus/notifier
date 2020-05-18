#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.fcm_client import FCMClient


class Exams(AbstractRoutine):
    def __init__(self):
        super().__init__("exams")

    def check(self, wilmaserver, wilmasession, push_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        fcm_client = FCMClient()
        exams = wilma_client.getExams()
        if exams.is_error():
            return exams.get_exception()
        offline_data_pt = self.get_file(push_id, push_id)
        if offline_data_pt is not None:
            offline_data = convertFromJSON(offline_data_pt)
            for l_exam in exams:
                found = False
                for o_exam in offline_data:
                    if o_exam['ExamId'] == l_exam['ExamId']:
                        found = True
                        break
                if not found:
                    push_content = {'type': 'notification', 'data': self.name, 'payload': l_exam}
                    fcm_client.sendPush(push_id, push_content)
                    print(convertToJSON(push_content))
        self.save_file(convertToJSON(exams.get_exams()), push_id, push_id)
        return None
