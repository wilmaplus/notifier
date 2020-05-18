#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

# Notifier configuration

API_KEY_CHECK_ENABLED = False
API_KEYS = []
ADMIN_PANEL = False

VALIDATE_CLIENT_KEY = False
VALID_CLIENT_PACKAGE = "com.example"

NOTIFIER_ROUTINES = [
    {'package': 'routines.exams', 'class': 'Exams'},
    {'package': 'routines.obs', 'class': 'Observations'},
    {'package': 'routines.news', 'class': 'News'}
]

# TODO set your FCM key(s)
FCM_SERVER_KEY = ""
IID_SERVER_KEY = ""
FCM_URL = "https://fcm.googleapis.com"
IID_URL = "https://iid.googleapis.com"
