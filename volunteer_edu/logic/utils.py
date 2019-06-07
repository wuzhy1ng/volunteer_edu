import base64
import random

from aliSDK.dysms_python.demo_sms_send import *

from logic.GLOBALVAR import *
from logic import users
from logic.expections import UserNotFountExpection


def getForm(request_post):
    """
    将QueryDict with json转化为普通的dict
    :param request_post: POST请求
    :return: 转化后的dict
    """
    form = {}
    for key, value in request_post.items():
        form[key] = value

    subjects = form.get('subjects', None)
    if subjects is not None:
        form['subjects'] = subjects.split(',')

    areas = form.get('areas', None)
    if areas is not None:
        form['areas'] = areas.split(',')

    print(form)
    return form


def sendSms(phone_number, sms_type):
    """
    向指定phone_number发送随机短信
    :param phone_number:手机号
    :return: code:验证码
    """
    business_id = uuid.uuid1()
    code = '%04d' % random.randint(1, 9999)
    params = "{\"code\":\"%s\"}" % code

    template_code = ''
    if sms_type == 'register_sms':
        template_code = APP_TEMPLATE_CODE_REGISTER
    elif sms_type == 'forget_sms':
        template_code = APP_TEMPLATE_CODE_FORGET

    send_sms(business_id,
             phone_number,
             APP_SIGN,
             template_code,
             params)

    return code


def saveImage(form):
    """
    上传头像
    :param data:
    :param phone_number:
    :return:
    """
    role = form['role']
    file = base64.b64decode(form['image'])
    phone_number = form['phone_number']

    # 保存文件
    image = IMG_PATH + role + '/' + phone_number
    with open(image, 'wb') as f:
        f.write(file)

    # 更新信息
    try:
        User = getattr(users, role)
        path = WEBSITE_ADDRESS + image
        form['image'] = path
        User(form).update()
    except UserNotFountExpection:
        pass

    return path


def saveCertification(form):
    """
    上传证书
    :param :form
    :param phone_number:
    :return:
    """

    # 保存文件
    file = base64.b64decode(form['certification'])
    phone_number = form['phone_number']
    certification = CERTIFICATION_PATH + phone_number
    with open(certification, 'wb') as f:
        f.write(file)

    # 更新信息
    try:
        User = getattr(users, 'Volunteer')
        path = WEBSITE_ADDRESS + certification
        form['certification'] = path
        User(form).update()
    except UserNotFountExpection:
        pass

    return path


def makeSession(request, form):
    request.session['is_login'] = True
    request.session['role'] = form['role']
    request.session['phone_number'] = form['phone_number']


def delSession(request):
    request.session['is_login'] = False
    request.session['role'] = ''
    request.session['phone_number'] = ''
