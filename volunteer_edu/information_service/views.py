from django.shortcuts import render, redirect
from django.http import JsonResponse

from information_service import models

from logic import users
from logic.expections import *
from logic.utils import *

import base64
from volunteer_edu import settings
import os


# Create your views here.

def register(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        print(form)
        try:
            User = getattr(users, form['role'])
            User(form).register()
            return JsonResponse({'message': '注册成功！'}, status=200)
        except UserExistedException:
            return JsonResponse({'exception': 'UserExistedException'}, status=403)


def register_sms(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        # 发送短信
        print(request.POST)
        form = getForm(request.POST)
        phone_number = form['phone_number']
        # code = sendSms(phone_number)
        code = '1111'
        return JsonResponse({'code': code}, status=200)


def register_safe(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        return JsonResponse({}, status=200)


def login(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
        # return render(request, 'login.html')
    elif request.method == 'POST':
        form = getForm(request.POST)
        print(form)

        try:
            User = getattr(users, form['role'])
            User(form).login()

            # 没有异常,给个session,跳转到home
            request.session['is_login'] = True
            request.session['role'] = form['role']
            request.session['phone_number'] = form['phone_number']

            return redirect('/index/home/')
        except UserNotFountExpection:
            return JsonResponse({'exception': 'UserNotFountExpection'}, status=403)
        except UserUnavailableExpection:
            return JsonResponse({'exception': 'UserUnavailableExpection'}, status=403)
        except PasswordErrorExpection:
            return JsonResponse({'exception': 'PasswordErrorExpection'}, status=403)


def logout(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        del request.session['is_login']
        del request.session['role']
        del request.session['phone_number']
        return JsonResponse({}, status=200)


def home(request):
    if request.method == 'GET':
        if request.session.get('is_login'):
            form = {'role': request.session.get('role'),
                    'phone_number': request.session.get('phone_number')}

            User = getattr(users, form['role'])
            user_message, user_image = User(form).home()
            return JsonResponse({'message': user_message, 'image': user_image}, status=200)
        else:
            return redirect('/index/login/')


def test(request):
    if request.method == 'POST':
        print(request.POST)
        form = getForm(request.POST)
        print(form)

        # image = base64.b64decode(form['image'])
        # with open('static/test.jpg') as f:
        #     f.write(image)

        # print(request.POST)
        # form = request.POST
        # image = form['image']
        # imagedata = base64.b64decode(image)
        # file_path = os.path.join(settings.STATICFILES_DIRS, '222.jpg')
        # file = open(file_path, "wb")
        # file.write(imagedata)
        # file.close()
        return JsonResponse({'path': 'http://47.105.150.105:8000/static/test.jpg'}, status=200)


def update_message(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        User = getattr(users, form['role'])
        User(form).update()
        return JsonResponse({}, status=200)


def update_image(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':

        form = getForm(request.POST)
        print(form)

        # 将头像存到文件里
        image_data = form['image']
        phone_number = form['phone_number']
        path = saveImage(image_data, phone_number)

        # 将路径写到数据库
        models.Volunteer.objects.filter(phone_number=phone_number).update(image=path)

        file_url = request.build_absolute_uri(path)

        return JsonResponse({'file_url': file_url}, status=200)


def update_certification(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':

        form = getForm(request.POST)

        # 将头像存到文件里
        certification_data = form['certification']
        phone_number = form['phone_number']
        path = saveCertification(certification_data, phone_number)

        # 将路径写到数据库
        models.Volunteer.objects.filter(phone_number=phone_number).update(certification=path)

        file_url = request.build_absolute_uri('/' + path)

        return JsonResponse({'file_url': file_url}, status=200)
