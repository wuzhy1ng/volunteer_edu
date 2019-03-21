from django import forms


class RegisterForm(forms.Form):
    is_vaild = forms.BooleanField(required=True)
    phone_number = forms.CharField(required=True, max_length=12)
    password = forms.CharField(required=True, max_length=16)
    name = forms.CharField(required=True, max_length=16)
    gender = forms.BooleanField(required=True)  # 性别
    wechat = forms.CharField(required=True, max_length=32)  # 微信号
    hometown = forms.CharField(required=True, max_length=16)  # 籍贯
    school = forms.CharField(required=True, max_length=32)  # 学校
    majority = forms.CharField(required=True, max_length=8)  # 专业
    identify = forms.CharField(required=True, max_length=4)  # 目前身份（大学几年级）
    address = forms.CharField(required=True, max_length=32)  # 地址
    image = forms.FilePathField(required=True)
    title = forms.CharField(max_length=32)
