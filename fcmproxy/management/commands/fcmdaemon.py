#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import asyncio
import json
import logging
from multiprocessing import Process

import websockets
from django.conf import settings
from django.core.management.base import BaseCommand

from fcmproxy.models import PersistentId, ForwardingSubscriber, SubscriberDevice
from fcmproxy.utils import forward_to_device
from asgiref.sync import sync_to_async


def get_persistent_ids():
    return list(PersistentId.objects.values_list('persistent_id'))

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)

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
    def on_notification(notification, persistent_id):
        if settings.DEBUG:
            print(persistent_id)

        try:
            if PersistentId.objects.filter(persistent_id=persistent_id).exists():
                return
        except Exception as e:
            print(e)

        if notification is not None and notification['data'] is not None:
            # Process notification, get all subscriber devices and forward
            subscriber_filter = ForwardingSubscriber.objects.filter(wilma_url=notification['data']['url'],
                                                                    wilma_uid=int(notification['data']['id']),
                                                                    wilma_usertype=int(notification['data']['type']))
            if subscriber_filter.exists():
                subscriber = subscriber_filter.first()
                Command.relay_notification(notification['data'], subscriber)

        # store in persistent ID storage
        persistent_id_db = PersistentId.objects.create()
        persistent_id_db.persistent_id = persistent_id
        persistent_id_db.save()



    async def process_incoming_message(self, message, websocket):
        try:
            json_data = json.loads(message)
            if "request" in json_data:
                request = json_data["request"]
                if request == "get-persistent-ids":
                    db_persistent_ids = await sync_to_async(get_persistent_ids, thread_sensitive=True)()
                    persistent_ids = []
                    for persistent_id in db_persistent_ids:
                        persistent_ids.append("".join(persistent_id))
                    if settings.DEBUG:
                        print("Persistent IDs from DB: {}".format(len(persistent_ids)))
                    await websocket.send(json.dumps({"success": True, "request": request, "response": persistent_ids}))
            elif "notification" in json_data:
                notification = json_data["notification"]
                persistent_id = json_data["persistentId"]
                await sync_to_async(self.on_notification, thread_sensitive=True)(notification, persistent_id)
            elif "credentials" in json_data:
                creds = json_data["credentials"]
                print("New FCM Key: {}".format(creds["fcm"]["token"]))

        except Exception as e:
            print("Parsing failed", e)
            print(e)
            logger.error(e)
            await websocket.send(json.dumps({"success": False, "request": "unknown", "response": e.__str__()}))

    async def web_socket_listener(self, uri):
        async with websockets.connect(uri) as websocket:
            async for message in websocket:
                await self.process_incoming_message(message, websocket)

    def handle(self, *args, **options):
        asyncio.run(self.web_socket_listener(settings.FCMPROXY_HOST))
