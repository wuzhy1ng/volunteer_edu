from apscheduler.schedulers.background import BackgroundScheduler
from information_service.models import Volunteer, Student
from reservation_service.models import Reservation, VolunteerMessage, StudentMessage
from recommend_service.models import SearchTrail
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max
from logic import GLOBALVAR
from math import sqrt


def sendMessage(reservation):
    volunteer = reservation.volunteer
    student = reservation.student

    StudentMessage.objects.create(is_readed=False,
                                  reservation_state=-1,
                                  time=timezone.now(),
                                  source=' 系统管理员 ',
                                  student=student,
                                  reservation=reservation,
                                  )
    if volunteer is not None:
        VolunteerMessage.objects.create(is_readed=False,
                                        reservation_state=-1,
                                        time=timezone.now(),
                                        source=' 系统管理员 ',
                                        volunteer=volunteer,
                                        reservation=reservation,
                                        )


# ------------------------我是一条分割线----------------------------

scheduler = BackgroundScheduler()


def test_job():
    print("I'm a test job!")


def confirmingReservationClear():
    """
    定时清理待确定的预约订单，若超过7*24小时（一周）或超过预约时间未确认，订单失效
    同时学生（和志愿者--如果有的话)都收到消息
    :return:
    """
    print('confirming reservation clearing')
    now = datetime.now()
    time_limit = timedelta(days=7)
    reservations = Reservation.objects.all()
    for each in reservations:
        if each.state == 0:
            delta = now - each.last_update_time

            # 超过预约时间未确认
            hour_and_minute = each.start_time.split(':')
            service_time = datetime(year=each.service_data.year,
                                    month=each.service_data.month,
                                    day=each.service_data.day,
                                    hour=int(hour_and_minute[0]),
                                    minute=int(hour_and_minute[1]),
                                    )

            if delta > time_limit or service_time < now:
                each.state = -1
                each.last_update_time = timezone.now()
                sendMessage(each)  # 发消息给学生（和志愿者--如果有的话)
                each.save()
    print('confirming reservation cleared')


def finishingReservationClear():
    """
    定时清理志愿当天未确认的订单的预约订单，若超过7*24小时（一周）未确认，订单失效
    同时志愿者和学生都收到消息
    :return:
    """
    print('finishing reservation clearing')
    now = datetime.now()
    time_limit = timedelta(days=7)
    reservations = Reservation.objects.all()
    for each in reservations:
        if each.state == 1:
            delta = now - each.last_update_time
            if delta > time_limit:
                each.state = -1
                each.last_update_time = timezone.now()
                sendMessage(each)  # 发消息给志愿者和学生
                each.save()
    print('finishing reservation cleared')


def searchTrailClear():
    """
    清理超过7*24小时（一周）的用户轨迹
    :return:
    """
    print('searchTrail clearing')
    now = datetime.now()
    time_limit = timedelta(days=7)
    search_trails = SearchTrail.objects.all()
    for each in search_trails:
        delta = now - each.time
        if delta > time_limit:
            each.delete()
    print('searchTrail cleared')


def messageClear():
    """
    清理三天以上已读信息
    :return:
    """
    print('message clearing')
    now = datetime.now()
    time_limit = timedelta(days=3)
    volunteer_messages = VolunteerMessage.objects.all()
    for each in volunteer_messages:
        if each.is_readed:
            delta = now - each.time
            if delta > time_limit:
                each.delete()
    student_message = StudentMessage.objects.all()
    for each in student_message:
        if each.is_readed:
            delta = now - each.time
            if delta > time_limit:
                each.delete()
    print('message cleared')


def updateItemCF():
    """
    更新物品（志愿者）协同过滤矩阵
    :return:
    """
    print('updating ItemCF')
    # 创建协同过滤矩阵和喜欢（预约）次数向量
    volunteer_number = Volunteer.objects.all().aggregate(Max('id'))['id__max']
    N = [0 for i in range(0, volunteer_number + 1)]
    GLOBALVAR.ItemCF = [[0 for i in range(0, volunteer_number + 1)]
                        for j in range(0, volunteer_number + 1)]

    # 获取所有学生
    students = Student.objects.all()
    for student in students:
        # 获得某个学生预约过的所有志愿者
        reservations = student.reservation_set.all()

        # 预约情况统计
        volunteer_list = list()
        for reservation in reservations:
            if reservation.volunteer is not None:
                volunteer_list.append(reservation.volunteer.id)
                N[reservation.volunteer.id] += 1

        # 列表去重
        volunteer_list = list(set(volunteer_list))

        # 获得共同喜欢（预约）的志愿者矩阵
        for i in range(0, len(volunteer_list)):
            for j in range(i + 1, len(volunteer_list)):
                GLOBALVAR.ItemCF[volunteer_list[i]][volunteer_list[j]] += 1
                GLOBALVAR.ItemCF[volunteer_list[j]][volunteer_list[i]] += 1

    # 生成协同过滤矩阵并按列归一化
    for j in range(1, volunteer_number + 1):
        maxVal = 0
        for i in range(1, volunteer_number + 1):
            if GLOBALVAR.ItemCF[i][j] != 0:
                GLOBALVAR.ItemCF[i][j] /= sqrt(N[i] * N[j])
                maxVal = max(maxVal, GLOBALVAR.ItemCF[i][j])
        if maxVal != 0:
            for i in range(1, volunteer_number + 1):
                GLOBALVAR.ItemCF[i][j] /= maxVal

    print('updated ItemCF')


# 启动定时任务
scheduler.add_job(updateItemCF, 'cron', hour=0, id='updateItemCF')  # 午夜0点更新
scheduler.add_job(confirmingReservationClear, 'cron', minute=10, id='confirmingReservationClear')
scheduler.add_job(finishingReservationClear, 'cron', minute=20, id='finishingReservationClear')
scheduler.add_job(searchTrailClear, 'cron', minute=30, id='searchTrailClear')
scheduler.add_job(messageClear, 'cron', minute=40, id='messageClear')

scheduler.start()
