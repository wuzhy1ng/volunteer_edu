from information_service.models import Volunteer
from reservation_service.models import Reservation
from reservation_service.models import StudentMessage
from reservation_service.models import VolunteerMessage
from django.utils import timezone


def confirmReservation(form):
    id = form['id']
    success = int(form['success'])

    # 针对可能存在的公告式预约，确认时需要获取志愿者手机号
    volunteer_phone_number = form.get('volunteer_phone_number', None)

    reservation = Reservation.objects.get(id=id)
    if success == 1:
        # 确认订单
        reservation.state = 1
        reservation.last_update_time = timezone.now()

        # 向订单添加志愿者（公告式预约）
        if volunteer_phone_number is not None:
            volunteer = Volunteer.objects.get(phone_number=volunteer_phone_number)
            reservation.volunteer = volunteer

        reservation.save()
        message = '订单已确认'
        code = 1
    else:
        # 订单取消
        reservation.state = -1
        reservation.last_update_time = timezone.now()
        reservation.save()
        message = '订单取消'
        code = -1

    # 学生收到消息
    StudentMessage.objects.create(reservation=reservation,
                                  reservation_state=reservation.state,
                                  time=timezone.now(),
                                  source=reservation.volunteer.name,
                                  student=reservation.student,
                                  )
    # 志愿者收到消息
    VolunteerMessage.objects.create(reservation=reservation,
                                    reservation_state=reservation.state,
                                    time=timezone.now(),
                                    source=reservation.student.name,
                                    volunteer=reservation.volunteer,
                                    )

    return message, code
