#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import asyncio
import json
import os.path
from uuid import uuid4

from .classes import *
from aioapns import APNs, NotificationRequest, PushType
from django.conf import settings


class APNSClient:

    def __init__(self):
        self.apns_client = APNs(
            key=os.path.join(settings.BASE_DIR, settings.APNS_PRIVATE_KEY_FILENAME),
            key_id=settings.APNS_KEY_ID,
            team_id=settings.APPLEDEV_TEAM_ID,
            topic=settings.APNS_TOPIC,
            use_sandbox=settings.APNS_DEV,
        )

    def send_push(self, device_id, data, push_type, priority=5, expiration=0):
        notif_request = NotificationRequest(
            device_token=device_id,
            message=data,
            notification_id=str(uuid4()),
            time_to_live=expiration,
            priority=str(priority),
            push_type=push_type,
        )
        loop = asyncio.get_event_loop()
        notification_result = loop.run_until_complete(self.apns_client.send_notification(notif_request))
        if notification_result.is_successful is not True:
            return ErrorResult(exception="id: {0}, {1} {2}".format(notification_result.notification_id, notification_result.status, notification_result.description))
        return PushSendRequest(notification_result.is_successful)
