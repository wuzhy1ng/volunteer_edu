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
    list_per_page = 15
    list_filter = (
        'is_vaild',
        'gender',
    )
    search_fields = (
        'phone_number',
        'name',
    )
    filter_horizontal = ('subjects', 'areas')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'phone_number',
                    'password',
                    'name',
                    'grade',
                    'address',
                    'wechat',
                    )
    list_per_page = 15
    search_fields = (
        'phone_number',
        'name',
    )


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'type')
    list_per_page = 15


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_per_page = 15


class VolunteerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'volunteer', 'text')
    list_per_page = 15


class StudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'text')
    list_per_page = 15


admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(VolunteerFeedback, VolunteerFeedbackAdmin)
admin.site.register(StudentFeedback, StudentFeedbackAdmin)
