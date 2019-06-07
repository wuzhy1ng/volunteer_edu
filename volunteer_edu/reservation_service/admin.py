from django.contrib import admin
from reservation_service.models import *


# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service_data',
        'duration',
        'state',
        'subject',
        'address',
        'volunteer',
        'student',
        'start_time',
        'create_time',
        'last_update_time',
    )
    list_per_page = 15


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text',)
    list_per_page = 15


class VolunteerMessageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'is_readed',
                    'reservation',
                    'reservation_state',
                    'time',
                    'volunteer',
                    )


class StudentMessageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'is_readed',
                    'reservation',
                    'reservation_state',
                    'time',
                    'student',
                    )


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(VolunteerMessage, VolunteerMessageAdmin)
admin.site.register(StudentMessage, StudentMessageAdmin)
