from django.db import models
from django.utils import timezone

from information_service.models import Volunteer, Student


# Create your models here.
class Reservation(models.Model):
    volunteer_read = models.BooleanField(default=False, verbose_name='志愿者是否已读')
    student_read = models.BooleanField(default=False, verbose_name='学生是否已读')
    volunteer_finished = models.BooleanField(default=False, verbose_name='志愿者确认完成')
    student_finished = models.BooleanField(default=False, verbose_name='学生确认完成')

    service_data = models.DateField(default=timezone.now, blank=True, verbose_name='服务日期')
    start_time = models.CharField(default=timezone.now, max_length=32, verbose_name='开始辅导时间')
    duration = models.FloatField(default=0, verbose_name='持续时长')
    state = models.IntegerField(default=-1, verbose_name='状态')
    subject = models.CharField(max_length=64, verbose_name='学科名')  # 这里与学科关联是否更合理
    address = models.CharField(max_length=32, verbose_name='辅导地址')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='订单创建时间')
    last_update_time = models.DateTimeField(default=timezone.now, verbose_name='最后更新时间')

    volunteer = models.ForeignKey(Volunteer, null=True, on_delete=models.CASCADE, verbose_name='志愿者')
    student = models.ForeignKey(Student, default=1, on_delete=models.CASCADE, verbose_name='学生')

    class Meta:
        verbose_name = '家教预约订单'
        verbose_name_plural = '家教预约订单'

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    text = models.CharField(max_length=100, verbose_name='内容')
    volunteer = models.ForeignKey(Volunteer, default=1, on_delete=models.CASCADE, verbose_name='志愿者')
    student = models.ForeignKey(Student, default=1, on_delete=models.CASCADE, verbose_name='学生')
    time = models.DateTimeField(default=timezone.now, verbose_name='时间')

    reservation = models.OneToOneField('Reservation', default=1, on_delete=models.CASCADE, verbose_name='订单')

    class Meta:
        verbose_name = '订单评价'
        verbose_name_plural = '订单评价'

    def __str__(self):
        return self.text


class VolunteerMessage(models.Model):
    is_readed = models.BooleanField(default=False, verbose_name='是否已读')
    reservation_state = models.IntegerField(default=1, verbose_name='订单状态')
    time = models.DateTimeField(default=timezone.now, verbose_name='时间')
    source = models.CharField(max_length=16, blank=True, verbose_name='消息来源')

    volunteer = models.ForeignKey(Volunteer, default=1, on_delete=models.CASCADE, verbose_name='志愿者')
    reservation = models.ForeignKey('Reservation', default=1, on_delete=models.CASCADE, verbose_name='关联订单')

    class Meta:
        verbose_name = '志愿者消息'
        verbose_name_plural = '志愿者消息'


class StudentMessage(models.Model):
    is_readed = models.BooleanField(default=False, verbose_name='是否已读')
    reservation_state = models.IntegerField(default=1, verbose_name='订单状态')
    time = models.DateTimeField(default=timezone.now, verbose_name='时间')
    source = models.CharField(max_length=16, blank=True, verbose_name='消息来源')

    student = models.ForeignKey(Student, default=1, on_delete=models.CASCADE, verbose_name='学生')
    reservation = models.ForeignKey('Reservation', default=1, on_delete=models.CASCADE, verbose_name='关联订单')

    class Meta:
        verbose_name = '学生消息'
        verbose_name_plural = '学生消息'
