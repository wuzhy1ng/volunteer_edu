from information_service.models import Volunteer, Student, Subject
from recommend_service.models import SearchTrail
from logic import GLOBALVAR
from django.db.models import Q, Max
from django.core import serializers
import random
import datetime
import json

top_N = 5
random_volunteers_number = 100


def randomVolunteers():
    '''
    随机获取100个志愿者
    :return:
    '''
    # 得到最大数量
    maxNum = Volunteer.objects.all().aggregate(Max('id'))['id__max']

    # 不足100个直接全部返回
    if maxNum < random_volunteers_number:
        return Volunteer.objects.filter(is_vaild=True)

    # 随机获取100个志愿者
    else:
        volunteers_id = Q()
        for i in range(1, random_volunteers_number + 1):
            volunteers_id = volunteers_id | Q(id=random.randint(1, maxNum + 1))
        return Volunteer.objects.filter(volunteers_id & Q(is_vaild=True))


def recentTrail(student):
    '''
    获得最近七天的100条用户轨迹
    :param student:
    :return:
    '''
    start = datetime.datetime.now() - datetime.timedelta(days=7)
    end = datetime.datetime.now()
    trails = SearchTrail.objects.filter(student=student, time__range=(start, end)).order_by('time')
    if trails.count() < 100:
        return trails
    else:
        return trails[0:100]


def itemCFRecommend(student, volunteers, recommend_score):
    '''
    基于协同过滤的推荐
    :param student:
    :param volunteers:
    :param recommend_score: 推荐得分
    :return:
    '''
    if GLOBALVAR.ItemCF is None:
        from information_service.scheduler import updateItemCF
        updateItemCF()

    # 获取学生所有历史订单中预约过的志愿者
    reservations = student.reservation_set.all()
    history_volunteer_list = list()
    for reservation in reservations:
        if reservation.volunteer is not None:
            history_volunteer_list.append(reservation.volunteer.id)

    # 志愿者去重
    history_volunteer_list = list(set(history_volunteer_list))

    # 依照历史预约志愿者推荐
    for volunteer_id in recommend_score:
        for history_volunteer in history_volunteer_list:
            recommend_score[volunteer_id] += GLOBALVAR.ItemCF[history_volunteer][volunteer_id]


def contentRecommend(student, volunteers, recommend_score):
    '''
    基于内容的推荐--以学科偏好为主
    :param student:
    :param volunteers:
    :param recommend_score:
    :return:
    '''
    search_trails = recentTrail(student)  # 获取近期用户轨迹

    # 偏好分布向量，索引0元素表示近期点击最大值
    subject_max = Subject.objects.all().aggregate(Max('id'))['id__max']
    subject_vec = [0 for i in range(0, subject_max + 1)]

    # 获取学生点击量
    for trail in search_trails.iterator():
        subjects = trail.volunteer.subjects.all()
        for subject in subjects.iterator():
            subject_vec[subject.id] += 1

    # 获取学生偏好分布（归一化）
    for i in range(1, len(subject_vec)):
        subject_vec[0] = max(subject_vec[0], subject_vec[i])
    if subject_vec[0] != 0:  # 防止无轨迹数据
        for i in range(1, len(subject_vec)):
            subject_vec[i] /= subject_vec[0]

    # 用偏好分布和热度评估志愿者
    for volunteer in volunteers:
        # 偏好分布评分
        subjects = volunteer.subjects.all()
        for subject in subjects.iterator():
            recommend_score[volunteer.id] += subject_vec[subject.id]

        # 热度评分
        recommend_score[volunteer.id] += volunteer.star_number / (1 + volunteer.star_number)


def recommendVolunteers(form):
    '''
    推荐志愿者
    推荐规则：基于内容的推荐 + 基于协同过滤的推荐
    :param form:
    :return:
    '''
    print(form['student_phone_number'])
    student = Student.objects.get(phone_number=form['student_phone_number'])

    volunteers = randomVolunteers()  # 获取随机志愿者
    recommend_score = dict()  # 生成得分字典
    for volunteer in volunteers:
        recommend_score[volunteer.id] = 0

    # 从抽取的志愿者中获取推荐的志愿者
    contentRecommend(student, volunteers, recommend_score)
    itemCFRecommend(student, volunteers, recommend_score)

    # 通过得分排序得到元祖列表
    recommend_score = sorted(recommend_score.items(), key=lambda x: x[1], reverse=True)

    # 抽取top-N志愿者
    recommend_Q = Q()
    for i in range(0, top_N):
        recommend_Q = recommend_Q | Q(id=recommend_score[i][0])

    volunteers = Volunteer.objects.filter(recommend_Q)
    volunteers = serializers.serialize('json', volunteers, use_natural_foreign_keys=True,
                                       fields=(
                                           'name',
                                           'school',
                                           'majority',
                                           'title',
                                           'phone_number',
                                           'gender',
                                           'identify',
                                           'subjects',
                                           'areas',
                                           'star_number',
                                           'description',
                                           'image',
                                       ))

    # 把得分元祖列表转换回字典
    recommend_score = dict(recommend_score)

    # 为志愿者添加得分
    volunteers = json.loads(volunteers)
    for volunteer in volunteers:
        volunteer['fields']['score'] = recommend_score[volunteer['pk']]
    volunteers = json.dumps(volunteers)

    return volunteers
