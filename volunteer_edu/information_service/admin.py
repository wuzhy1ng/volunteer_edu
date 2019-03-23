from django.contrib import admin
from information_service.models import *


# Register your models here.


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'is_vaild',
                    'phone_number',
                    'password',
                    'name',
                    'gender',
                    'wechat',
                    'hometown',
                    'school',
                    'majority',
                    'identify',
                    'address',
                    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'phone_number',
                    'password',
                    'name',
                    'grade',
                    'address',
                    'wechat',
                    )


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(History)
admin.site.register(Comment)
admin.site.register(Area, AreaAdmin)
