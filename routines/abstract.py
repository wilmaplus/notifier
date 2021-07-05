#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
from wplusnotifier_storage.storage import *
import json
from datetime import datetime
from django.conf import settings


def filterFunc(item, date_key, date_format):
    dateString = item[date_key]
    date_time_obj = datetime.strptime(dateString, date_format)
    comparison = datetime.now() - date_time_obj
    return comparison.days < settings.MAX_TIMESTAMP


def filterItemsByDate(array, date_key, date_format="%Y-%m-%d"):
    return list(filter(lambda item: filterFunc(item, date_key, date_format), array))


def convertFromJSON(content):
    return json.loads(content)


def convertToJSON(content):
    return json.dumps(content)


class AbstractRoutine:

    def __init__(self, name, filename=None):
        self.name = name
        self.filename = name
        if filename is not None:
            self.filename = filename

    def check(self, wilmaserver, wilmasession, push_id, user_id):
        raise Exception("check method should be overridden! If you already did it, remove the super method")

    def get_file(self, enc_pass, push_id, user_id):
        return get_saved_data(enc_pass, self.filename, push_id, user_id)

    def save_file(self, content, enc_pass, push_id, user_id):
        return save_data(content, enc_pass, self.filename, push_id, user_id)

    def delete_file(self, push_id, user_id):
        return delete_saved_data(self.filename, push_id, user_id)
