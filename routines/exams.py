#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from .abstract import AbstractRoutine


class Exams(AbstractRoutine):
    def __init__(self, push_utils):
        super().__init__("exams", push_utils)

    def check(self, wilmaserver, wilmasession, enc_pass, push_id):
        pass



