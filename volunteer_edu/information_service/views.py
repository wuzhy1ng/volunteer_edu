from django.http import JsonResponse
from logic.expections import *
from logic.utils import *
from logic.information_actions.SearchVolunteers import searchVolunteers
from logic.information_actions.SearchAllVolunteers import searchAllVolunteers
from logic.information_actions.SearchDetailVolunteer import searchDetailVolunteer
from logic.information_actions.UploadFeedback import uploadFeedback


# Create your views here.

def register(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        try:
            User = getattr(users, form['role'])
            User(form).register()
            return JsonResponse({'message': '注册成功！'}, status=200)
        except UserExistedException:
            return JsonResponse({'exception': 'UserExistedException'}, status=201)


def register_sms(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        # 发送短信
        form = getForm(request.POST)
        phone_number = form['phone_number']
        code = sendSms(phone_number, 'register_sms')
        # code = '1111'
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
        try:
            User = getattr(users, form['role'])
            User(form).login()
            # 没有异常,给个session
            makeSession(request, form)
            return JsonResponse({'message': '登录成功'}, status=200)
        except UserNotFountExpection:
            return JsonResponse({'exception': 'UserNotFountExpection'}, status=201)
        except UserUnavailableExpection:
            return JsonResponse({'exception': 'UserUnavailableExpection'}, status=201)
        except PasswordErrorExpection:
            return JsonResponse({'exception': 'PasswordErrorExpection'}, status=201)


def logout(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        delSession(request)
        return JsonResponse({'message': '登出成功'}, status=200)


def home(request):
    if request.method == 'POST':
        # 用session登录
        if request.session.get('is_login', None) is not None and request.session['is_login']:
            form = {'role': request.session['role'],
                    'phone_number': request.session['phone_number']}
        else:
            form = getForm(request.POST)
        User = getattr(users, form['role'])
        user_message = User(form).home()
        return JsonResponse({'message': user_message}, status=200)


def update_message(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        User = getattr(users, form['role'])
        User(form).update()
        return JsonResponse({'message': '信息更新成功'}, status=200)


def update_image(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        path = saveImage(form)
        return JsonResponse({'message': '头像上传成功', 'file_url': path}, status=200)


def update_certification(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        path = saveCertification(form)
        return JsonResponse({'message': '认证上传成功', 'file_url': path}, status=200)


def search(request):
    if request.method == 'GET':
        volunteers = searchAllVolunteers()
        return JsonResponse({'volunteers': volunteers}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        volunteers = searchVolunteers(form)
        return JsonResponse({'volunteers': volunteers}, status=200)


def search_detail(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)

        # 记录学生轨迹
        if request.session.get('role', None) is not None and request.session['role'] == 'Student':
            form['student_phone_number'] = request.session['phone_number']

        message = searchDetailVolunteer(form)
        return JsonResponse({'message': message}, status=200)


def forget(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        try:
            User = getattr(users, form['role'])
            User(form).update()
            return JsonResponse({'message': '修改密码成功'}, status=200)
        except UserNotFountExpection:
            return JsonResponse({'exception': '用户不存在'}, status=201)


def forget_sms(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        # 发送短信
        form = getForm(request.POST)
        phone_number = form['phone_number']
        code = sendSms(phone_number, 'forget_sms')
        # code = '1111'
        return JsonResponse({'code': code}, status=200)


def feedback(request):
    if request.method == 'GET':
        return JsonResponse({}, status=200)
    elif request.method == 'POST':
        form = getForm(request.POST)
        uploadFeedback(form)
        return JsonResponse({'message': '反馈成功'}, status=200)


def test(request):
    if request.method == 'GET':
        from django.shortcuts import render
        return render(request, 'test.html')
    elif request.method == 'POST':
        from information_service.scheduler import updateItemCF
        from logic import GLOBALVAR

        updateItemCF()
        print(GLOBALVAR.ItemCF)

        return JsonResponse({}, status=200)


import information_service.scheduler
