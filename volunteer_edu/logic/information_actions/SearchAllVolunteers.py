from information_service.models import Volunteer
from django.core import serializers


def searchAllVolunteers():
    """
    返回所有志愿者信息
    :return:
    """
    querySet = Volunteer.objects.filter(is_vaild=True)
    volunteers = serializers.serialize('json', querySet, use_natural_foreign_keys=True,
                                       fields=('name',
                                               'school',
                                               'majority',
                                               'title',
                                               'phone_number',
                                               'gender',
                                               'identify',
                                               'subjects',
                                               'star_number',
                                               'description',
                                               'areas',
                                               'image',))

    return volunteers
