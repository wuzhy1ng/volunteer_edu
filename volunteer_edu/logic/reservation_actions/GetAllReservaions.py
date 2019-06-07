from reservation_service.models import Reservation
from django.core import serializers
import json


def getAllReservation():
    raw_reservations = Reservation.objects.filter(state=0, volunteer=None)
    reservations = serializers.serialize('json', raw_reservations, use_natural_foreign_keys=True)

    reservations = json.loads(reservations)

    # 返回id和学生头像
    for i in range(0, len(reservations)):
        reservations[i]['fields']['image'] = raw_reservations[i].student.image
        reservations[i]['fields']['phone_number'] = raw_reservations[i].student.phone_number
        reservations[i]['fields']['wechat'] = raw_reservations[i].student.wechat
        reservations[i]['fields']['id'] = raw_reservations[i].id

    reservations = json.dumps(reservations)

    return reservations
