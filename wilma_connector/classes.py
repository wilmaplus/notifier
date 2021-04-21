#  Copyright (c) 2020 openKirkes, developed by Developer From Jokela


class RequestResult:

    def __init__(self, error, exception=None, response=None):
        self.error = error
        self.exception = exception
        self.response = response
        if error and exception is None:
            raise Exception("Exception cannot be None when error is True")

    def get_exception(self):
        return self.exception

    def is_error(self):
        return self.error

    def get_response(self):
        return self.response


class ErrorResult(RequestResult):

    def __init__(self, exception, wilma_error=None):
        super().__init__(True, exception)
        self.wilma_error = wilma_error

    def get_wilma_error(self):
        return self.wilma_error


class LoginResult(RequestResult):

    def __init__(self, session):
        super().__init__(False, None, None)
        self.session = session

    def get_session(self):
        return self.session


class SessionValidateResult(RequestResult):

    def __init__(self, validation, user_id, user_type, wilma_id):
        super().__init__(False, None, None)
        self.validation = validation
        self.user_id = user_id
        self.user_type = user_type
        self.wilma_id = wilma_id

    def get_combined_user_id(self):
        return str(self.user_id) + "_" + str(self.user_type) + "_"+ self.wilma_id

    def is_valid_session(self):
        return self.validation


class PushSendRequest(RequestResult):

    def __init__(self, success):
        super().__init__(False, None, None)
        self.success = success

    def is_sent(self):
        return self.success


class PushDetailsRequest(RequestResult):

    def __init__(self, details):
        super().__init__(False, None, None)
        self.details = details

    def get_details(self):
        return self.details


class ExamsResult(RequestResult):

    def __init__(self, exams):
        super().__init__(False, None, None)
        self.exams = exams

    def get_exams(self):
        return self.exams

class MessagesResult(RequestResult):

    def __init__(self, messages):
        super().__init__(False, None, None)
        self.messages = messages

    def get_messages(self):
        return self.messages


class ObservationsResult(RequestResult):

    def __init__(self, observations, excuses_allowed):
        super().__init__(False, None, None)
        self.observations = observations
        self.excusesAllowed = excuses_allowed

    def isExcusesAllowed(self):
        return self.excusesAllowed

    def get_observations(self):
        return self.observations


class NewsResult(RequestResult):

    def __init__(self, news):
        super().__init__(False, None, None)
        self.news = news

    def get_news(self):
        return self.news
