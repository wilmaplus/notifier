#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

class AbstractRoutine:

    def __init__(self, name, push_utils, filename=None):
        self.name = name
        self.filename = name
        self.push_utils = push_utils
        if filename is not None:
            self.filename = filename

    def check(self, wilmaserver, wilmasession, enc_pass, push_id):
        raise Exception("check method should be overridden! If you already did it, remove the super method")
