from recommend_service.models import SearchTrail
from django.utils import timezone


def recordTrail(volunteer, student):
    SearchTrail.objects.create(volunteer=volunteer,
                               student=student,
                               time=timezone.now(),
                               )
