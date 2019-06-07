from information_service import models
from django.utils import timezone


def uploadFeedback(form):
    text = form['text']
    role = form['role']
    phone_number = form['phone_number']

    User = getattr(models, role)
    user = User.objects.get(phone_number=phone_number)
    if role == 'Volunteer':
        models.VolunteerFeedback.objects.create(text=text,
                                                volunteer=user,
                                                time=timezone.now())
    elif role == 'Student':
        models.StudentFeedback.objects.create(text=text,
                                              student=user,
                                              time=timezone.now())
