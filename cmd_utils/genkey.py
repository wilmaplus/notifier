#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

# This file generates a Secret Key for the Settings

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())