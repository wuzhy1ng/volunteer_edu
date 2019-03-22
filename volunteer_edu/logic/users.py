from information_service import models
from logic.expections import *
from logic.GLOBALVAR import *

import json


class Volunteer:

    def __init__(self, form, file=None):
        self.form = form
        self.file = file

    def register(self):
        """
        注册对象
        :return:
        :exception:UserExistedException
        """

        # 查重
        if models.Volunteer.objects.filter(phone_number=self.form['phone_number']).count() != 0:
            raise UserExistedException()

        # 创建ORM对象
        volunteer = models.Volunteer.objects.create(
            is_vaild=False,
            phone_number=self.form['phone_number'],
            password=self.form['password'],
            name=self.form['name'],
            gender=self.form['gender'],
            wechat=self.form['wechat'],
            hometown=self.form['hometown'],
            school=self.form['school'],
            majority=self.form['majority'],
            identify=self.form['identify'],
            address=self.form['address'],
            title=self.form['title'],
        )

        # 将外键关系加入用户信息
        for each in self.form['subjects']:
            subject = models.Subject.objects.get(name=each)
            volunteer.subjects.add(subject)
        for each in self.form['areas']:
            area = models.Area.objects.get(name=each)
            volunteer.areas.add(area)

        # 头像保存（如果有的话)
        if self.file is not None:
            image_format = self.file.split('.')[1]
            path = IMG_PATH + volunteer.name + image_format
            with open(path, 'wb') as f:
                for line in self.file.chunks():
                    f.write(line)
            volunteer.image = path
        else:
            volunteer.image = ''

        volunteer.save()

    def login(self):
        """
        用户登陆
        :return:
        :exception:
            UserNotFountExpection,
            UserUnavailableExpection,
            PasswordErrorExpection,
        """
        # 检查用户是否存在
        if models.Volunteer.objects.filter(phone_number=self.form['phone_number']).count() == 0:
            raise UserNotFountExpection()

        volunteer = models.Volunteer.objects.get(phone_number=self.form['phone_number'])
        # 检查用户是否可用
        if volunteer.is_vaild is False:
            raise UserUnavailableExpection()
        if volunteer.password != self.form['password']:
            raise PasswordErrorExpection()

        return volunteer

    def home(self):
        return models.Volunteer.objects.get(phone_number=self.form['phone_number'])


class Student:

    def __init__(self, form, file=None):
        self.form = form
        self.file = file

    def register(self):
        """
        注册对象
        :return:
        :exception:UserExistedException
        """

        # 查重
        if models.Student.objects.filter(phone_number=self.form['phone_number']).count() != 0:
            raise UserExistedException()

        # 创建ORM对象
        student = models.Student.objects.create(
            phone_number=self.form['phone_number'],
            password=self.form['password'],
            name=self.form['name'],
            grade=self.form['grade'],
            address=self.form['address'],
            wechat=self.form['wechat'],
        )

        # 头像保存（如果有的话)
        if self.file is not None:
            image_format = self.file.split('.')[1]
            path = IMG_PATH + student.name + image_format
            with open(path, 'wb') as f:
                for line in self.file.chunks():
                    f.write(line)
            student.image = path
        else:
            student.image = ''

        student.save()

    def login(self):
        """
                用户登陆
                :return:
                :exception:
                    UserNotFountExpection,
                    PasswordErrorExpection,
                """
        # 检查用户是否存在
        if models.Student.objects.filter(phone_number=self.form['phone_number']).count() == 0:
            raise UserNotFountExpection()

        student = models.Student.objects.get(phone_number=self.form['phone_number'])
        # 检查用户是否可用
        if student.password != self.form['password']:
            raise PasswordErrorExpection()

        return student

    def home(self):
        return models.Student.objects.get(phone_number=self.form['phone_number'])
