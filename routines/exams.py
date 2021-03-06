#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine, convertToJSON, convertFromJSON
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.fcm_client import FCMClient


class Exams(AbstractRoutine):
    def __init__(self):
        super().__init__("exams")

    def check(self, wilmaserver, wilmasession, push_id, user_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        fcm_client = FCMClient()
        exams = wilma_client.getExams()
        if exams.is_error():
            return exams
        offline_data_pt = self.get_file(push_id, push_id, user_id)
        user_object = {'user_id': user_id.split("_")[0], 'user_type': user_id.split("_")[1], 'server': wilmaserver}
        if offline_data_pt is not None:
            offline_data = convertFromJSON(offline_data_pt)
            for l_exam in exams.get_exams():
                found = False
                gradeChange = False
                for o_exam in offline_data:
                    if o_exam['ExamId'] == l_exam['ExamId']:
                        found = True
                        o_grade = o_exam.get('Grade', None)
                        l_grade = l_exam.get('Grade', None)
                        if l_grade is not None and o_grade is not None:
                            if l_grade != o_grade:
                                gradeChange = True
                        elif l_grade is not None:
                            gradeChange = True
                        break
                if not found:
                    push_content = {'type': 'notification', 'data': self.name, 'payload': l_exam}
                    push_content.update(user_object)
                    fcm_client.sendPush(push_id, push_content)
                elif gradeChange:
                    push_content = {'type': 'notification', 'data': self.name+"_grade", 'payload': l_exam}
                    push_content.update(user_object)
                    fcm_client.sendPush(push_id, push_content)
        self.save_file(convertToJSON(exams.get_exams()), push_id, push_id, user_id)
        return None
