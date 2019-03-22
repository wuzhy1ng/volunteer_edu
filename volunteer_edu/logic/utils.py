import json


def getForm(request_post):
    """
    将QueryDict with json转化为普通的dict
    :param request_post: POST请求
    :return: 转化后的dict
    """
    form = {}
    for key, value in request_post.items():
        # print(key,value)
        form[key] = json.loads(value)
    return form
