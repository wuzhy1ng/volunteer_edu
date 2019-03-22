from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from logic import users
from logic.expections import *
from logic.utils import *

import json


# Create your views here.

def register(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    elif request.method == 'POST':
        form = getForm(request.POST)

        try:
            User = getattr(users, form['role'])
            User(form).register()
            return HttpResponse(json.dumps('Ok'), status=200)
        except UserExistedException:
            return HttpResponse(json.dumps('UserExisted'), status=403)


def login(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    elif request.method == 'POST':
        form = getForm(request.POST)

        try:
            User = getattr(users, form['role'])
            user = User(form).login()
            return HttpResponse(json.dumps({'user': user}), status=200)

        except UserNotFountExpection:
            return HttpResponse(json.dumps('UserNotFount', status=403))

        except UserUnavailableExpection:
            return HttpResponse(json.dumps('UserUnavailable', status=403))

        except PasswordErrorExpection:
            return HttpResponse(json.dumps('PasswordError', status=403))


def home(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    elif request.method == 'POST':
        json_data = request.POST['json']
        form = json.dumps(json_data)

        User = getattr(users, form['role'])
        user_home = User(form).home()
        return HttpResponse(json.dumps(user_home), status=200)
