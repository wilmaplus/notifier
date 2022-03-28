#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf import settings
import importlib


def runRoutines(wilma_server, wilma_session, push_key, user_id, to_skip=None):
    if to_skip is None:
        to_skip = []
    routines = settings.NOTIFIER_ROUTINES
    for routine in routines:
        routineID = routine['code']
        try:
            routineClass = importlib.import_module(routine['package'])
            class_ = getattr(routineClass, routine['class'])
            if routineID not in to_skip:
                class_().check(wilma_server, wilma_session, push_key, user_id)
            else:
                class_().delete_file(push_key, user_id)
        except:
            print(f"Failed {routineID}")


def deleteRoutineFiles(push_key, user_id):
    routines = settings.NOTIFIER_ROUTINES
    for routine in routines:
        routineClass = importlib.import_module(routine['package'])
        class_ = getattr(routineClass, routine['class'])
        class_().delete_file(push_key, user_id)
