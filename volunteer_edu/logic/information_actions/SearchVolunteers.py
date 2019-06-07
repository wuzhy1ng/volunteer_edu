from django.db.models import Q
from information_service.models import Volunteer, Student
from logic.recommend_actions.RecommendVolunteers import itemCFRecommend
from django.core import serializers
import json


def searchVolunteers(form):
    """
    查询符合条件的所有志愿者 -- 模糊查询 + 协同过滤推荐
    :param form:
    :return: 序列化的志愿者集合
    """

    keyword = form.get('keyword', None)
    volunteers = Volunteer.objects.filter(is_vaild=True)
    for item in keyword:
        volunteers = volunteers.filter(
            Q(subjects__name__contains=item) |
            Q(subjects__grade__contains=item) |
            Q(subjects__type__contains=item) |
            Q(areas__name__contains=item) |
            Q(name__contains=item)
        ).distinct()

    # 协同过滤推荐
    if form.get('student_phone_number', None) is not None:
        student = Student.objects.get(phone_number=form['student_phone_number'])
        recommend_score = dict()
        for volunteer in volunteers:
            recommend_score[volunteer.id] = 0
        itemCFRecommend(student, volunteers, recommend_score)

    volunteers = serializers.serialize('json', volunteers, use_natural_foreign_keys=True,
                                       fields=('name',
                                               'school',
                                               'majority',
                                               'title',
                                               'phone_number',
                                               'description',
                                               'star_number',
                                               'gender',
                                               'identify',
                                               'subjects',
                                               'areas',
                                               'image',))

    # 添加协同过滤得分
    if form.get('student_phone_number', None) is not None:
        volunteers = json.loads(volunteers)
        for volunteer in volunteers:
            volunteer['fields']['score'] = recommend_score[volunteer['pk']]
        volunteers = json.dumps(volunteers)

    return volunteers
