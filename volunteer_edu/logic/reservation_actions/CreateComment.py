from reservation_service.models import Comment, Reservation, VolunteerMessage
from django.utils import timezone


def createComment(form):
    id = int(form['id'])
    text = form['text']
    star = int(form['star'])

    # 创建评论
    reservation = Reservation.objects.get(id=id)
    reservation.state = 2
    reservation.last_update_time = timezone.now()
    reservation.save()
    Comment.objects.create(text=text,
                           volunteer=reservation.volunteer,
                           student=reservation.student,
                           time=timezone.now(),
                           reservation=reservation,
                           )

    # 志愿者收到消息
    VolunteerMessage.objects.create(reservation_state=3,
                                    time=timezone.now(),
                                    source=reservation.student.name,
                                    volunteer=reservation.volunteer,
                                    reservation=reservation,
                                    )

    # 志愿者获赞
    if star == 1:
        volunteer = reservation.volunteer
        volunteer.star_number += 1
        volunteer.save()

    message = '评价成功'
    code = 2
    return message, code
