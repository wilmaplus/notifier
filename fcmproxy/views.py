# -*- coding: utf-8 -*-

#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

import json
import os
from pathlib import Path
from django.conf import settings
from rest_framework.decorators import permission_classes, api_view
from fcmproxy.utils import DeviceType
from fcmproxy.models import SubscriberDevice, ForwardingSubscriber
from wilma_connector.classes import ErrorResult
from wilma_connector.wilma_client import WilmaClient
from wplusnotifier_rest.views import checkApiKey, generateWilmaErrorResponse, generateResponse, generateErrorResponse


def get_fcm_key():
    file_path = Path(os.path.join(settings.STORAGE_DIR, 'fcm_cred.json'))
    try:
        with open(file_path, "r") as f:
            credentials = json.load(f)
            return credentials["fcm"]["token"]
    except FileNotFoundError:
        return None


@api_view(['POST'])
@permission_classes([])
def add(request):
    apikey_result = checkApiKey(request)
    if apikey_result.is_error():
        return generateErrorResponse(apikey_result)
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    push_type = request.data.get('push_type', None)
    push_key = request.data.get('push_key', None)

    # Validate input
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'), 400)
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'), 400)
    if push_type is None:
        return generateErrorResponse(ErrorResult('push_type integer is missing!'), 400)
    if push_key is None:
        return generateErrorResponse(ErrorResult('push_key is missing!'), 400)
    if not DeviceType.has_value(push_type):
        return generateErrorResponse(ErrorResult('Invalid push type'), 400)

    push_key = push_key.strip()
    push_type = int(push_type)

    # Check Wilma session
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.check_global_session()
    if session_check.is_error():
        return generateWilmaErrorResponse(session_check, session_check.get_wilma_error())
    else:
        proxy_fcm_key = get_fcm_key()
        if proxy_fcm_key is None:
            return generateErrorResponse(ErrorResult('FCM Service is unavailable right now. Please try again later'),
                                         500)

        # Add key to Wilma push list
        wilma_client.add_push_key(proxy_fcm_key)

        device = SubscriberDevice.objects.filter(type=push_type, key=push_key).first()
        if device is None:
            device = SubscriberDevice()
            device.key = push_key
            device.type = push_type
            device.save()

        # Update subscriber and device db
        if session_check.user_type != 7:
            db_subscriber = ForwardingSubscriber.objects.filter(wilma_url=wilma_client.http_client.get_plain_url(),
                                                                wilma_uid=session_check.user_id,
                                                                wilma_usertype=session_check.user_type).first()
            if db_subscriber is None:
                db_subscriber = ForwardingSubscriber()
                db_subscriber.wilma_url = wilma_client.http_client.get_plain_url()
                db_subscriber.wilma_uid = session_check.user_id
                db_subscriber.wilma_usertype = session_check.user_type
                db_subscriber.save()

            # Update device DB
            if not device.subscribers.filter(id=db_subscriber.id).exists():
                device.subscribers.add(db_subscriber)
        else:
            for role in session_check.roles:
                db_subscriber = ForwardingSubscriber.objects.filter(wilma_url=wilma_client.http_client.get_plain_url(),
                                                                    wilma_uid=role['PrimusId'],
                                                                    wilma_usertype=role['Type']).first()
                if db_subscriber is None:
                    db_subscriber = ForwardingSubscriber()
                    db_subscriber.wilma_url = wilma_client.http_client.get_plain_url()
                    db_subscriber.wilma_uid = role['PrimusId']
                    db_subscriber.wilma_usertype = role['Type']
                    db_subscriber.save()
                # Update device DB

                if not device.subscribers.filter(id=db_subscriber.id).exists():
                    device.subscribers.add(db_subscriber)
        return generateResponse({})


@api_view(['POST'])
@permission_classes([])
def remove(request):
    apikey_result = checkApiKey(request)
    if apikey_result.is_error():
        return generateErrorResponse(apikey_result)
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    push_type = int(request.data.get('push_type', None))
    push_key = request.data.get('push_key', None)

    # Validate input
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'), 400)
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'), 400)
    if push_type is None:
        return generateErrorResponse(ErrorResult('push_type integer is missing!'), 400)
    if push_key is None:
        return generateErrorResponse(ErrorResult('push_key is missing!'), 400)
    if not DeviceType.has_value(push_type):
        return generateErrorResponse(ErrorResult('Invalid push type'), 400)

    push_key = push_key.strip()

    # Check Wilma session
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.check_global_session()
    if session_check.is_error():
        return generateWilmaErrorResponse(session_check, session_check.get_wilma_error())
    else:
        proxy_fcm_key = get_fcm_key()
        if proxy_fcm_key is None:
            return generateErrorResponse(ErrorResult('FCM Service is unavailable right now. Please try again later'),
                                         500)

        # Add key to Wilma push list
        wilma_client.remove_push_key(proxy_fcm_key)

        device = SubscriberDevice.objects.filter(type=push_type, key=push_key).first()

        # Update subscriber and device db
        print(session_check.user_type)
        if session_check.user_type != 7:
            db_subscriber = ForwardingSubscriber.objects.filter(wilma_url=wilma_client.http_client.get_plain_url(),
                                                                wilma_uid=session_check.user_id,
                                                                wilma_usertype=session_check.user_type).first()
            if db_subscriber is None:
                return generateResponse({})

            # Update device DB
            if db_subscriber is not None:
                if device is not None and device.subscribers.filter(id=db_subscriber.id).exists():
                    device.subscribers.remove(db_subscriber)
                if SubscriberDevice.objects.filter(subscribers__id=db_subscriber.id).count() < 1:
                    db_subscriber.delete()
                if device is not None and device.subscribers.count() < 1:
                    device.delete()
        else:
            for role in session_check.roles:
                db_subscriber = ForwardingSubscriber.objects.filter(wilma_url=wilma_client.http_client.get_plain_url(),
                                                                    wilma_uid=role['PrimusId'],
                                                                    wilma_usertype=role['Type']).first()
                if db_subscriber is not None:
                    if device is not None and device.subscribers.filter(id=db_subscriber.id).exists():
                        device.subscribers.remove(db_subscriber)
                    if SubscriberDevice.objects.filter(subscribers__id=db_subscriber.id).count() < 1:
                        db_subscriber.delete()
                    if device is not None and device.subscribers.count() < 1:
                        device.delete()

        return generateResponse({})

