from django.db import models
from django.utils import timezone


# Create your models here.

class Volunteer(models.Model):
    is_vaild = models.BooleanField()  # 是否验证成功
    phone_number = models.CharField(max_length=12)  # 手机号
    password = models.CharField(max_length=16)  # 密码
    name = models.CharField(max_length=16)  # 姓名
    gender = models.CharField(max_length=2)  # 性别
    wechat = models.CharField(max_length=32)  # 微信号
    hometown = models.CharField(max_length=16)  # 籍贯
    school = models.CharField(max_length=32)  # 学校
    majority = models.CharField(max_length=8)  # 专业
    identify = models.CharField(max_length=4)  # 目前身份（大学几年级）
    address = models.CharField(max_length=32)  # 地址
    image = models.FilePathField()  # 头像
    certification = models.FilePathField()  # 学生证照片
    title = models.CharField(max_length=100)  # 荣誉称号

    subjects = models.ManyToManyField('Subject')  # 教授科目
    areas = models.ManyToManyField('Area')  # 可教授区域


class Student(models.Model):
    phone_number = models.CharField(max_length=12)  # 手机号
    password = models.CharField(max_length=16)  # 密码
    name = models.CharField(max_length=16)  # 姓名
    grade = models.CharField(max_length=10)  # 年级
    address = models.CharField(max_length=100)  # 地址
    image = models.FilePathField()  # 头像
    wechat = models.CharField(max_length=32)  # 微信


class Subject(models.Model):
    name = models.CharField(max_length=10)


class History(models.Model):
    subject = models.CharField(max_length=10)
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=timezone.now())

    volunteer = models.ForeignKey('Volunteer', on_delete=models.CASCADE, default=1)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, default=1)


class Comment(models.Model):
    text = models.CharField(max_length=100)

    volunteer = models.ForeignKey('Volunteer', on_delete=models.CASCADE, default=1)


class Area(models.Model):
    name = models.CharField(max_length=8)
