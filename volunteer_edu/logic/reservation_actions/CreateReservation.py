from reservation_service.models import Reservation, VolunteerMessage
from information_service.models import Volunteer, Student
from django.utils import timezone
import re


def getDate(time):
    print(time)
    res = re.match('(\d*)-(\d*)-(\d*)', time)
    res = res.groups()
    service_date = timezone.datetime(year=int(res[0]), month=int(res[1]), day=int(res[2]))
    return service_date


def getDuration(duration):
    return float(duration)


def createOneToOneReservation(form):
    subject = form['subject']
    service_data = getDate(form['serve_data'])
    start_time = form['start_time']
    duration = getDuration(form['duration'])
    volunteer = Volunteer.objects.get(phone_number=form['volunteer_phone_number'])
    student = Student.objects.get(phone_number=form['student_phone_number'])
    # 创建订单
    reservation = Reservation.objects.create(
        service_data=service_data,
        duration=duration,
        state=0,
        subject=subject,
        create_time=timezone.now(),
        last_update_time=timezone.now(),
        start_time=start_time,
        volunteer=volunteer,
        student=student,
    )
    # 志愿者获得消息
    VolunteerMessage.objects.create(
        reservation=reservation,
        reservation_state=reservation.state,
        time=timezone.now(),
        volunteer=volunteer,
        source=student.name,
    )


def createPublicReservation(form):
    subject = form['subject']
    service_data = getDate(form['serve_data'])
    start_time = form['start_time']
    duration = getDuration(form['duration'])
    address = form['address']
    student = Student.objects.get(phone_number=form['student_phone_number'])
    Reservation.objects.create(
        service_data=service_data,
        duration=duration,
        state=0,
        subject=subject,
        address=address,
        create_time=timezone.now(),
        last_update_time=timezone.now(),
        start_time=start_time,
        student=student,
    )


def createReservation(form):
    '''
    创建订单，可分为一对一预约和公开预约
    :param form:
    :return:
    '''

    # 一对一预约
    if form.get('volunteer_phone_number', None) is not None:
        createOneToOneReservation(form)

    # 公告式预约
    else:
        createPublicReservation(form)
