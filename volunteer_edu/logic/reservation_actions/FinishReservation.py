from reservation_service.models import Reservation
from reservation_service.models import StudentMessage, VolunteerMessage
from django.utils import timezone


def finishReservation(form):
    id = form['id']

    reservation = Reservation.objects.get(id=id)
    reservation.state = 2
    reservation.last_update_time = timezone.now()
    reservation.save()

    # 学生和志愿者收到消息
    VolunteerMessage.objects.create(reservation_state=2,
                                    time=timezone.now(),
                                    source=reservation.student.name,
                                    volunteer=reservation.volunteer,
                                    reservation=reservation,
                                    )
    StudentMessage.objects.create(reservation_state=2,
                                  time=timezone.now(),
                                  source=reservation.volunteer.name,
                                  student=reservation.student,
                                  reservation=reservation,
                                  )

    message = '订单已完成'
    code = 2

    return message, code
