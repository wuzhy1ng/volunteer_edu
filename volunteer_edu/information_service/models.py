from django.db import models


# Create your models here.

class Volunteer(models.Model):
    is_vaild = models.BooleanField()  # 是否验证成功
    phone_number = models.CharField(max_length=12)  # 手机号
    password = models.CharField(max_length=16)  # 密码
    name = models.CharField(max_length=16)  # 姓名
    gender = models.BooleanField()  # 性别
    wechat = models.CharField(max_length=32)  # 微信号
    hometown = models.CharField(max_length=16)  # 籍贯
    school = models.CharField(max_length=32)  # 学校
    majority = models.CharField(max_length=8)  # 专业
    identify = models.CharField(max_length=4)  # 目前身份（大学几年级）
    address = models.CharField(max_length=32)  # 地址
    image = models.FilePathField()  # 头像
    title = models.CharField(max_length=32)  # 荣誉称号

    edu_subjects = models.ManyToManyField('Subject')  # 教授科目
    edu_area = models.ManyToManyField('Area')  # 可教授区域
    edu_historys = models.ForeignKey('Edu_history', on_delete=models.CASCADE)  # 志愿记录
    edu_comments = models.ForeignKey('Edu_comment', on_delete=models.CASCADE)  # 所获志愿评价


class Student(models.Model):
    address = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    gender = models.BooleanField()
    name = models.CharField(max_length=32)
    image = models.FilePathField()
    phone_number = models.CharField(max_length=12)
    wechat = models.CharField(max_length=32)
    edu_historys = models.ForeignKey('Edu_history', on_delete=models.CASCADE)


class Subject(models.Model):
    name = models.CharField(max_length=10)


class Edu_history(models.Model):
    volunteer_name = models.CharField(max_length=32)
    student_name = models.CharField(max_length=32)
    subject = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Edu_comment(models.Model):
    text = models.CharField(max_length=100)

class Area(models.Model):
    name = models.CharField(max_length=8)

