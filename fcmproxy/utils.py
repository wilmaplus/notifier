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
        result = apns_client.send_push(device['key'],
                                       data, PushType.BACKGROUND)
        if result.is_error():
            print(result.get_exception())
        exit(0)
