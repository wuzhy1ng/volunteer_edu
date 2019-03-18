from django.db import models


# Create your models here.

class Volunteer(models.Model):
    is_vaild = models.BooleanField()
    school = models.CharField(max_length=32)
    class_name = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    gender = models.BooleanField()
    image = models.FilePathField()
    title = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=12)
    wechat = models.CharField(max_length=32)
    edu_historys = models.ForeignKey('Edu_history', on_delete=models.CASCADE)
    edu_comments = models.ForeignKey('Edu_comment', on_delete=models.CASCADE)
    edu_subjects = models.ManyToManyField('Subject')


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
