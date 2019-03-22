from django.shortcuts import render
from django.http import JsonResponse

from information_service import models
from information_service.forms import *

from logic import users
from logic.expections import *


# Create your views here.

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    elif request.method == 'POST':
        json_data = request.POST['json']
        form = json.loads(json_data)

        try:
            User = getattr(users, form['role'])
            User(form,request.FILES['file']).register()
        except UserExistedException:
            return JsonResponse('UserExisted')

        # raw_form = json.loads(json_data)
        #
        # form = RegisterForm(raw_form, request.FILES)
        # edu_subjects = raw_form['edu_subjects']
        # edu_areas = raw_form['edu_areas']
        #
        # # 若信息合法
        # if form.is_vaild() and edu_subjects and edu_areas:
        #
        #     # 查重
        #     if models.Volunteer.objects.filter(phone_number=form.phone_number).count() == 0:
        #         return HttpResponse(json.dumps('volunteer exited'))
        #
        #     # 用户信息写入数据库
        #     volunteer = models.Volunteer(is_vaild=form.is_vaild,
        #                                  phone_number=form.phone_number,
        #                                  password=form.password,
        #                                  name=form.name,
        #                                  gender=form.gender,
        #                                  wechat=form.wechat,
        #                                  hometown=form.hometown,
        #                                  school=form.school,
        #                                  majority=form.majority,
        #                                  identify=form.identify,
        #                                  address=form.address,
        #                                  title=form.title
        #                                  )
        #     # 将外键关系加入用户信息
        #     for each in edu_subjects:
        #         subject = models.Subject.objects.get(name=each)
        #         volunteer.edu_subjects.add(subject)
        #     for each in edu_areas:
        #         area = models.Subject.objects.get(name=each)
        #         volunteer.edu_areas.add(area)
        #
        #     # 头像保存
        #     image_format = request.FILES['file'].split('.')[1]
        #     path = IMG_PATH + volunteer.name + image_format
        #     with open(path, 'wb') as f:
        #         for line in request.FILES['file'].chunks():
        #             f.write(line)
        #     volunteer.image = path
        #
        #     volunteer.save()

        # 若信息非法
        else:
            return HttpResponse(json.dumps('false form'))


def login(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    elif request.method == 'POST':



        json_data = request.POST['json']
        message = json.loads(json_data)
        phone_number = message['phone_number']
        password = message['password']
        identity = message['identity']

        User = getattr(models, 'identity')
        # 检查是否存在该用户
        if User.objects.filter(phone_number=phone_number).count() == 0:
            return HttpResponse(json.dumps('user is not exited'))

        user = User.objects.get(phone_number=phone_number)
        # 检查密码是否符合
        if user.password != password:
            return HttpResponse(json.dumps('password error'))

        return HttpResponse(json.dumps(user))


def home(request):
    if request.method == 'GET':
        return HttpResponse('ok')
    elif request.method == 'POST':

