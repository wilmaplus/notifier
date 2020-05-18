#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
from wplusnotifier_storage.storage import *
import json

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

    def check(self, wilmaserver, wilmasession, push_id):
        raise Exception("check method should be overridden! If you already did it, remove the super method")

    def get_file(self, enc_pass, push_id):
        return get_saved_data(enc_pass, self.filename, push_id)

    def save_file(self, content, enc_pass, push_id):
        print("savin requestd")
        return save_data(content, enc_pass, self.filename, push_id)
