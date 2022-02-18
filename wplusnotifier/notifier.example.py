#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

# Notifier configuration

API_KEY_CHECK_ENABLED = False
API_KEYS = []
DJANGO_ADMIN_PANEL = False

# Ignore all items older than x days, to avoid false-positive notifications,
# because of issue https://github.com/wilmaplus/notifier/issues/3
MAX_TIMESTAMP = 7

VALIDATE_CLIENT_KEY = False
VALID_CLIENT_PACKAGE = "com.example.app"

# In Linux systems which have file encryption, filenames are limited by size. This uses shorter hashing algorithms if
# set to true.
SHORT_FILENAMES = False

NOTIFIER_ROUTINES = [
    {'package': 'routines.exams', 'class': 'Exams', 'code': 'exams'},
    {'package': 'routines.obs', 'class': 'Observations', 'code': 'obs'},
    {'package': 'routines.news', 'class': 'News', 'code': 'news'},
    {'package': 'routines.reservemessages', 'class': 'ReserveMessages', 'code': 'reservemessages'}
]

# TODO set your FCM key(s)
FCM_SERVER_KEY = ""
IID_SERVER_KEY = ""
FCM_URL = "https://fcm.googleapis.com"
IID_URL = "https://iid.googleapis.com"

# FCMProxy Configuration
# FCMProxy forwards Firebase cloud messages from Wilma server to ie. Apple PNS or other methods.

ENABLE_FCM_PROXY = False
SENDER_ID = ""

# TODO Configure Apple Push Notification Service
APNS_DEV = False
APNS_PRIVATE_KEY_FILENAME = ""
APNS_KEY_ID = ""
APPLEDEV_TEAM_ID = ""
APNS_TOPIC = ""