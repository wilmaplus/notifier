#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine
from wilma_connector.wilma_client import WilmaClient


class Exams(AbstractRoutine):
    def __init__(self, push_utils):
        super().__init__("exams", push_utils)

    def check(self, wilmaserver, wilmasession, enc_pass, push_id):
        wilma_client = WilmaClient(wilmaserver, wilmasession)
        exams = wilma_client.getExams()
        if not exams.is_error():
            return exams.get_exception()

        return None




