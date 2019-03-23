import json
import random
import base64
from aliSDK.dysms_python.demo_sms_send import *
from logic.GLOBALVAR import *


def getForm(request_post):
    """
    将QueryDict with json转化为普通的dict
    :param request_post: POST请求
    :return: 转化后的dict
    """
    form = {}
    for key, value in request_post.items():
        # key = json.loads(key)
        form[key] = value

    subjects = form.get('subjects', None)
    if subjects is not None:
        form['subjects'] = subjects.split(',')

    areas = form.get('areas', None)
    if subjects is not None:
        form['areas'] = areas.split(',')

    return form


def sendSms(phone_number):
    """
    向指定phone_number发送随机短信
    :param phone_number:手机号
    :return: code:验证码
    """
    business_id = uuid.uuid1()
    code = '%04d' % random.randint(1, 9999)
    params = "{\"code\":\"%s\"}" % code

    send_sms(business_id,
             phone_number,
             APP_SIGN,
             APP_TEMPLATE_CODE,
             params)

    return code


def saveImage(data, phone_number):
    """
    上传头像
    :param data:
    :param phone_number:
    :return:
    """
    file = base64.b64decode(data)
    path = IMG_PATH + phone_number + '.jpg'
    with open(path, 'wb') as f:
        f.write(file)
    return path


def saveCertification(data, phone_number):
    """
    上传证书
    :param data:
    :param phone_number:
    :return:
    """
    file = base64.b64decode(data)
    path = CERTIFICATION_PATH + phone_number + '.jpg'
    with open(path, 'wb') as f:
        f.write(file)
    return path
