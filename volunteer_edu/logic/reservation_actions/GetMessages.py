from reservation_service.models import VolunteerMessage, StudentMessage
from django.core import serializers
import json


def getMessages(form):
    role = form['role']
    phone_number = form['phone_number']

    if role == 'Volunteer':
        raw_messages = VolunteerMessage.objects.filter(volunteer__phone_number=phone_number)
        messages = serializers.serialize('json', raw_messages,
                                         fields=(
                                             'is_readed',
                                             'reservation',
                                             'source',
                                             'time',
                                         ))
    elif role == 'Student':
        raw_messages = StudentMessage.objects.filter(student__phone_number=phone_number)
        messages = serializers.serialize('json', raw_messages,
                                         fields=(
                                             'is_readed',
                                             'reservation',
                                             'source',
                                             'time',
                                         ))

    # 杨老板说这里要加id，emmmmm。。代码就很拉闸
    messages = json.loads(messages)
    for i in range(0, len(messages)):
        messages[i]['fields']['id'] = raw_messages[i].id
    messages = json.dumps(messages)

    return messages
