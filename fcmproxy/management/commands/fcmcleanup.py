#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
from django.core.management import BaseCommand

from fcmproxy.models import PersistentId


class Command(BaseCommand):

    def handle(self, *args, **options):
        PersistentId.objects.all().delete()
        print("All persistent IDs removed")
