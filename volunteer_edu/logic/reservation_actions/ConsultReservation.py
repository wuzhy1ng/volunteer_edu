from reservation_service.models import Reservation
from reservation_service.models import StudentMessage, VolunteerMessage
from django.utils import timezone


def consultReservation(form):
    id = form['id']
    success = form['success']

    reservation = Reservation.objects.get(id=id)
    if success is True:
        # 确认已协商订单
        reservation.state = 2
        reservation.save()
        message = '订单协商完成'
        code = 2
    else:
        # 订单取消
        reservation.state = -1
        reservation.save()
        message = '订单取消'
        code = -1

    # 志愿者收到消息
    VolunteerMessage.objects.create(reservation_id=reservation.id,
                                    reservation_state=reservation.state,
                                    time=timezone.now(),
                                    volunteer=reservation.volunteer,
                                    )

    # 学生收到消息
    StudentMessage.objects.create(reservation_id=reservation.id,
                                  reservation_state=reservation.state,
                                  time=timezone.now(),
                                  student=reservation.student,
                                  )

    return message, code
