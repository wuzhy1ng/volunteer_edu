from django.shortcuts import render, HttpResponse

import json
from information_service.models import *
from information_service.forms import *

# Create your views here.

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    elif request.method == 'POST':
        json_data = request.POST['json']
        raw_form = json.loads(json_data)

        form = RegisterForm(request.POST)
        edu_subjects = raw_form['edu_subjects']
        edu_area = raw_form['edu_area']

        if form.is_vaild() and edu_subjects and edu_area:
            Volunteer.objects.create()


def login(request):
    return HttpResponse('ok')


def home(request):
    return HttpResponse('ok')
