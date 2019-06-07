from reservation_service.models import VolunteerMessage, StudentMessage, Reservation
from django.core import serializers


def getMessageDetail(form):
    role = form['role']
    id = int(form['id'])

    # 查看详细信息以后标记为已读
    if role == 'Volunteer':
        message = VolunteerMessage.objects.get(id=id)
        message.is_readed = True
        message.reservation.volunteer_read = True
        message.save()
        message = [message, ]

    elif role == 'Student':
        message = StudentMessage.objects.get(id=id)
        message.is_readed = True
        message.reservation.student_read = True
        message.save()
        message = [message, ]

    message = serializers.serialize('json', message, use_natural_foreign_keys=True)

    return message
