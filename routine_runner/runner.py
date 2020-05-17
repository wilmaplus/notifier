#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf import settings


def runRoutines(wilma_server, wilma_session, enc_password, push_key):
    routines = settings.NOTIFIER_ROUTINES
    for routine in routines:
        routineClass = eval(routine)
        routineClass.check(wilma_server, wilma_session, enc_password, push_key)
