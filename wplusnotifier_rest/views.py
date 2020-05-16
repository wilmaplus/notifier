# -*- coding: utf-8 -*-

#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import *


@api_view(['POST'])
@permission_classes([])
def push(request):
    generateResponse({})


def generateErrorResponse(error_result):
    return generateError(str(error_result.get_exception()))


def generateError(cause):
    base = baseResponse()
    base.update({'cause': cause})
    return Response(base)


def generateResponse(data):
    base = baseResponse(True)
    base.update(data)
    return Response(base)


def baseResponse(status=False):
    return {
        'status': status
    }
