from django.db import models
from logic.GLOBALVAR import *
from information_service.model_managers import *
from django.utils import timezone


# from reservation_service.models import Reservation, Comment


# Create your models here.

class Volunteer(models.Model):
    objects = VolunteerManager()
    is_vaild = models.BooleanField(verbose_name='验证是否通过')  # 是否验证成功
    phone_number = models.CharField(max_length=12, verbose_name='手机号')  # 手机号
    password = models.CharField(max_length=16, verbose_name='密码')  # 密码
    name = models.CharField(max_length=16, verbose_name='姓名')  # 姓名
    gender = models.CharField(max_length=2, verbose_name='性别')  # 性别
    wechat = models.CharField(max_length=32, verbose_name='微信号')  # 微信号
    hometown = models.CharField(max_length=16, verbose_name='籍贯')  # 籍贯
    school = models.CharField(max_length=32, verbose_name='学校')  # 学校
    majority = models.CharField(max_length=16, verbose_name='专业')  # 专业
    identify = models.CharField(max_length=4, verbose_name='目前身份')  # 目前身份（大学几年级）
    address = models.CharField(max_length=32, verbose_name='地址')  # 地址
    image = models.CharField(default=DEFAULT_VOLUNTEER_IMAGE_PATH, verbose_name='头像', max_length=128)  # 头像
    certification = models.CharField(default=DEFAULT_STUDENT_IMAGE_PATH, verbose_name='学生证照片',
                                     max_length=128)  # 学生证照片
    title = models.CharField(default='', max_length=100, verbose_name='荣誉称号')  # 荣誉称号
    description = models.CharField(default='', max_length=100, verbose_name='自我描述')
    star_number = models.IntegerField(default=0, verbose_name='获赞数')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    subjects = models.ManyToManyField('Subject', verbose_name='教授科目')  # 教授科目
    areas = models.ManyToManyField('Area', verbose_name='可教授区域')  # 可教授区域

    class Meta:
        verbose_name = '志愿者'
        verbose_name_plural = '志愿者库'

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class Student(models.Model):
    objects = StudentManager()

    phone_number = models.CharField(max_length=12, verbose_name='手机号')  # 手机号
    password = models.CharField(max_length=16, verbose_name='密码')  # 密码
    name = models.CharField(max_length=16, verbose_name='姓名')  # 姓名
    grade = models.CharField(max_length=10, verbose_name='年级')  # 年级
    address = models.CharField(max_length=100, verbose_name='地址')  # 地址
    image = models.CharField(default=DEFAULT_STUDENT_IMAGE_PATH, max_length=128, verbose_name='头像')  # 头像
    wechat = models.CharField(max_length=32, verbose_name='微信')  # 微信
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生库'

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class Subject(models.Model):
    objects = SubjectManager()

    name = models.CharField(max_length=16, unique=True, verbose_name='学科名')
    grade = models.CharField(max_length=8, blank=True, verbose_name='年级')
    type = models.CharField(max_length=8, blank=True, verbose_name='学科类型')

    class Meta:
        verbose_name = '学科'
        verbose_name_plural = '学科'

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class Area(models.Model):
    objects = AreaManager()

    name = models.CharField(max_length=8, unique=True, verbose_name='地区名')

    class Meta:
        verbose_name = '地区'
        verbose_name_plural = '地区'

    def natural_key(self):
        return self.name

    def __str__(self):
        return self.name


class VolunteerFeedback(models.Model):
    text = models.CharField(max_length=100, verbose_name='意见内容')
    volunteer = models.ForeignKey('Volunteer', on_delete=models.CASCADE, verbose_name='志愿者')
    time = models.DateTimeField(default=timezone.now, verbose_name='时间')

    class Meta:
        verbose_name = '来自志愿者的反馈'
        verbose_name_plural = '来自志愿者的反馈'

    def __str__(self):
        return str(self.id)


class StudentFeedback(models.Model):
    text = models.CharField(max_length=100, verbose_name='意见内容')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name='学生')
    time = models.DateTimeField(default=timezone.now, verbose_name='时间')

    class Meta:
        verbose_name = '来自学生的反馈'
        verbose_name_plural = '来自学生的反馈'

    def __str__(self):
        return str(self.id)
