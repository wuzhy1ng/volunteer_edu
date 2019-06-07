from django.db import models
from information_service.models import Volunteer, Student
import datetime


# Create your models here.

class SearchTrail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='学生')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, verbose_name='志愿者')
    time = models.DateTimeField(default=datetime.datetime.now, verbose_name='轨迹时间')

    class Meta:
        verbose_name = '学生点击行为轨迹'
        verbose_name_plural = '学生点击行为轨迹'
