from django.core import serializers

from information_service import models
from logic.expections import *
from logic.GLOBALVAR import *

import os


class Volunteer:

    def __init__(self, form):
        self.form = form

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
            description=self.form['description'],
        )

        # 将外键关系加入用户信息
        for each in self.form['subjects']:
            subject = models.Subject.objects.get(name=each)
            volunteer.subjects.add(subject)
        for each in self.form['areas']:
            area = models.Area.objects.get(name=each)
            volunteer.areas.add(area)

        # 存储image
        image_list = os.listdir(IMG_PATH + 'Volunteer/')
        for image in image_list:
            if image.startswith(self.form['phone_number']):
                image_path = WEBSITE_ADDRESS + IMG_PATH + 'Volunteer/' + image
                volunteer.image = image_path
                break

        # 存储certification
        certification_list = os.listdir(CERTIFICATION_PATH)
        for certification in certification_list:
            if certification.startswith(self.form['phone_number']):
                certification_path = WEBSITE_ADDRESS + CERTIFICATION_PATH + certification
                volunteer.certification = certification_path
                break

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

    def home(self):
        """
        获得个人信息，包括文字信息和图片信息
        :return:
            message(only 1 element list),
            image(encode with utf-8)
        """
        volunteer = models.Volunteer.objects.filter(phone_number=self.form['phone_number'])
        volunteer = serializers.serialize('json', volunteer, use_natural_foreign_keys=True)
        return volunteer

    def update(self):
        """
        更新个人信息
        :return:
        :exception:UserNotFountExpection
        """

        if models.Volunteer.objects.filter(phone_number=self.form['phone_number']).count() == 0:
            raise UserNotFountExpection

        if self.form.get('role', None) is not None:
            del self.form['role']

        # 更新地区（如果有的话）
        areas = self.form.get('areas', None)
        if areas is not None:
            volunteer = models.Volunteer.objects.get(phone_number=self.form['phone_number'])
            volunteer.areas.clear()
            for each in areas:
                area = models.Area.objects.get(name=each)
                volunteer.areas.add(area)
            volunteer.save()
            del self.form['areas']

        # 更新学科（如果有的话）
        subjects = self.form.get('subjects', None)
        if subjects is not None:
            volunteer = models.Volunteer.objects.get(phone_number=self.form['phone_number'])
            volunteer.subjects.clear()
            for each in subjects:
                subject = models.Subject.objects.get(name=each)
                volunteer.subjects.add(subject)
            volunteer.save()
            del self.form['subjects']

        models.Volunteer.objects.filter(phone_number=self.form['phone_number']).update(**self.form)


class Student:

    def __init__(self, form, file=None):
        self.form = form
        self.file = file

    def register(self):
        """
        注册对象
        :return:
        :exception:
            UserExistedException
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

        image_list = os.listdir(IMG_PATH + 'Student/')
        for image in image_list:
            if image.startswith(self.form['phone_number']):
                image_path = WEBSITE_ADDRESS + IMG_PATH + 'Student/' + image
                student.image = image_path
                break

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

    def home(self):
        """
        获得个人信息
        :return:
            message(only 1 element list),
            image(encode with utf-8)
        """
        student = models.Student.objects.filter(phone_number=self.form['phone_number'])
        student = serializers.serialize('json', student, use_natural_foreign_keys=True)

        return student

    def update(self):
        """
        更新个人信息（不包括图片）
        :return:
        """
        if self.form.get('role', None) is not None:
            del self.form['role']
        models.Student.objects.filter(phone_number=self.form['phone_number']).update(**self.form)
