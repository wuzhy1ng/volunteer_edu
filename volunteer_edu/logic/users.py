from information_service import models
from logic.expections import *
from logic.GLOBALVAR import *


class Volunteer:
    def __init__(self, form, file):
        self.form = form
        self.file = file

    def register(self):
        """
        注册对象
        :return:
        :exception:UserExistedException
        """

        # 查重
        if models.Volunteer.filter(phone_number=self.form['phone_number']).count() != 0:
            raise UserExistedException()

        # 创建ORM对象
        volunteer = models.Volunteer(is_vaild=False,
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
                                     image=self.form['image'],
                                     title=self.form['title'],
                                     )
        # 将外键关系加入用户信息
        for each in self.form['subjects']:
            subject = models.Subject.objects.get(name=each)
            volunteer.edu_subjects.add(subject)
        for each in self.form['areas']:
            area = models.Subject.objects.get(name=each)
            volunteer.edu_areas.add(area)

        # 头像保存
        image_format = self.file.split('.')[1]
        path = IMG_PATH + volunteer.name + image_format
        with open(path, 'wb') as f:
            for line in self.file.chunks():
                f.write(line)
        volunteer.image = path

        volunteer.save()
