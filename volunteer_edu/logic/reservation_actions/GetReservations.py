from information_service import models
from reservation_service.models import Reservation, VolunteerMessage, StudentMessage, Comment
from django.core import serializers
import json


def getReservations(form):
    role = form['role']
    # 按id查询
    if form.get('id', None) is not None:
        raw_reservation = Reservation.objects.filter(id=form['id'])
        # 已读状态更新
        if role == 'Volunteer':
            raw_reservation.update(volunteer_read=True)
            VolunteerMessage.objects.filter(reservation=raw_reservation[0]).update(is_readed=True)
        elif role == 'Student':
            raw_reservation.update(student_read=True)
            StudentMessage.objects.filter(reservation=raw_reservation[0]).update(is_readed=True)

        reservation = serializers.serialize('json', raw_reservation, use_natural_foreign_keys=True)
        reservation = json.loads(reservation)

        # 添加对方联系方式
        if role == 'Volunteer':
            reservation[0]['fields']['phone_number'] = raw_reservation[0].student.phone_number
            reservation[0]['fields']['wechat'] = raw_reservation[0].student.wechat
        elif role == 'Student' and raw_reservation[0].volunteer is not None:
            reservation[0]['fields']['phone_number'] = raw_reservation[0].volunteer.phone_number
            reservation[0]['fields']['wechat'] = raw_reservation[0].volunteer.wechat

        # 添加评论（如果有的话）
        if raw_reservation[0].state == 2:
            comment = raw_reservation[0].comment
            comment = serializers.serialize('json', [comment, ], use_natural_foreign_keys=True)
            comment = json.loads(comment)
            reservation[0]['fields']['comment'] = comment[0]['fields']

        reservation = json.dumps(reservation)

        return reservation

    # 按用户及其状态查询
    else:
        phone_number = form['phone_number']
        state = int(form.get('state', -2))

        User = getattr(models, role)
        user = User.objects.get(phone_number=phone_number)
        if state == -2:
            raw_reservations = user.reservation_set.all().order_by('last_update_time')
        else:
            raw_reservations = user.reservation_set.filter(state=state)

        # 返回带有订单id，对方联系方式的订单
        reservations = serializers.serialize('json', raw_reservations, use_natural_foreign_keys=True)

        reservations = json.loads(reservations)
        for i in range(0, len(reservations)):
            reservations[i]['fields']['id'] = raw_reservations[i].id
        reservations = json.dumps(reservations)

        return reservations
