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

    def __init__(self, exception):
        super(ErrorResult, self).__init__(True, exception)


class LoginResult(RequestResult):

    def __init__(self, session):
        super(LoginResult, self).__init__(False, None, None)
        self.session = session

    def get_session(self):
        return self.session


class SessionValidateResult(RequestResult):

    def __init__(self, validation):
        super(SessionValidateResult, self).__init__(False, None, None)
        self.validation = validation

    def is_valid_session(self):
        return self.validation


class ExamsResult(RequestResult):

    def __init__(self, exams):
        super(ExamsResult, self).__init__(False, None, None)
        self.exams = exams

    def get_exams(self):
        return self.exams


class ObservationsResult(RequestResult):

    def __init__(self, observations):
        super(ObservationsResult, self).__init__(False, None, None)
        self.observations = observations

    def get_observations(self):
        return self.observations


class NewsResult(RequestResult):

    def __init__(self, news):
        super(NewsResult, self).__init__(False, None, None)
        self.news = news

    def get_news(self):
        return self.news