#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf import settings
import json
from pathlib import Path
import os
from push_receiver import register, listen
from fcmproxy.models import PersistentId, ForwardingSubscriber, SubscriberDevice
from django.core.management.base import BaseCommand
from fcmproxy.utils import forward_to_device
from wplusnotifier_storage.storage import savePathCheck
from multiprocessing import Process


class Command(BaseCommand):

    @staticmethod
    def relay_notification(data, subscriber):
        subscriber_devices = SubscriberDevice.objects.filter(subscribers=subscriber)
        for device in subscriber_devices:
            pure_device = {"key": device.key, "type": device.type}
            p = Process(target=forward_to_device, args=(data, pure_device))
            p.start()
            # forward_to_device(data, device)

    @staticmethod
    def on_notification(obj, notification, data_message):
        persistent_id = data_message.persistent_id
        if settings.DEBUG:
            print(persistent_id)
        if PersistentId.objects.filter(persistent_id=persistent_id).exists():
            return

        # store in persistent ID storage
        persistent_id_db = PersistentId.objects.create()
        persistent_id_db.persistent_id = persistent_id
        persistent_id_db.save()

        if notification is not None and notification['data'] is not None:
            # Process notification, get all subscriber devices and forward
            subscriber_filter = ForwardingSubscriber.objects.filter(wilma_url=notification['data']['url'],
                                                                    wilma_uid=int(notification['data']['id']),
                                                                    wilma_usertype=int(notification['data']['type']))
            if subscriber_filter.exists():
                subscriber = subscriber_filter.first()
                Command.relay_notification(notification['data'], subscriber)

    def handle(self, *args, **options):
        sender_id = settings.SENDER_ID
        file_path = Path(os.path.join(settings.STORAGE_DIR, 'fcm_cred.json'))
        try:
            # already registered, load previous credentials
            with open(file_path, "r") as f:
                credentials = json.load(f)

        except FileNotFoundError:
            # first time, register and store credentials
            credentials = register(sender_id=sender_id)
            savePathCheck(settings.STORAGE_DIR)
            with open(file_path, "w") as f:
                json.dump(credentials, f)

        print("FCM Key: {}".format(credentials["fcm"]["token"]))

        db_persistent_ids = PersistentId.objects.values_list('persistent_id')
        persistent_ids = []
        for persistent_id in db_persistent_ids:
            persistent_ids.append("".join(persistent_id))
        if settings.DEBUG:
            print("Persistent IDs from DB: {}".format(len(persistent_ids)))
        listen(credentials, self.on_notification, persistent_ids)
