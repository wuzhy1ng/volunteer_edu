from information_service.models import Volunteer, Student
from logic.recommend_actions.RecordTrail import recordTrail
from django.core import serializers


def searchDetailVolunteer(form):
    """
    查询某个phone_number下的详细信息
    :param phone_number:
    :return: 仅有某个志愿者信息的序列化集合
    """
    message = {}
    phone_number = form['phone_number']
    volunteer = Volunteer.objects.filter(phone_number=phone_number)
    reservations = volunteer[0].reservation_set.all().order_by('-last_update_time').filter(state=2)
    comments = volunteer[0].comment_set.all()

    # 序列化三类数据
    volunteer = serializers.serialize('json', volunteer, use_natural_foreign_keys=True)
    reservations = serializers.serialize('json', reservations, use_natural_foreign_keys=True)
    comments = serializers.serialize('json', comments, use_natural_foreign_keys=True)

    # 存入message对象
    message['volunteer'] = volunteer
    message['reservations'] = reservations
    message['comments'] = comments

    # 记录学生轨迹
    if form.get('student_phone_number', None) is not None:
        student = Student.objects.get(phone_number=form['student_phone_number'])
        volunteer = Volunteer.objects.get(phone_number=form['phone_number'])
        recordTrail(volunteer, student)

    return message
