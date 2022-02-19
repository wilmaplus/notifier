#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
from enum import Enum

from aioapns import PushType

from wilma_connector.apns_client import APNSClient


class DeviceType(Enum):
    APPLE = 1


    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def forward_to_device(data, device):
    if device['type'] == 1:
        # APNS
        apns_client = APNSClient()
        category = "UNKNOWN"
        if "m_id" in data:
            category = "WILMA_MESSAGE"
        title = "Uusi viesti"
        body = "Avaa viesti klikkaamalla"
        if "title" in data and "message" in data:
            title = data["title"]
            body = data["message"]
        apple_data = {
            "aps": {
                "category": category,
                "mutable-content": 1,
                "alert": {
                    "title": title,
                    "body": body
                }
            },
            "data": data
        }
        result = apns_client.send_push(device['key'],
                                       apple_data, PushType.ALERT)
        if result.is_error():
            print(result.get_exception())
        exit(0)
