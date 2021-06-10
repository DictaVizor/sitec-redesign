from django.db import models
from django.contrib.auth.models import User

class StudentSitecData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    panel_data = models.TextField()
    log_data = models.TextField()
    reinscription_data = models.TextField()
    cycle_advance_data = models.TextField()
    kardex_data = models.TextField()
    log_data = models.TextField()

    @property
    def owner(self):
        return self.user



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    plan = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    score = models.IntegerField()
    credits = models.IntegerField()
    entry_period = models.CharField(max_length=255)
    validated_periods = models.IntegerField()
    last_period = models.CharField(max_length=255)
    tutor = models.CharField(max_length=255)

    curp = models.CharField(max_length=255)
    birthdate = models.DateTimeField()
    address = models.CharField(max_length=255)
    home_phone = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    origin_school = models.CharField(max_length=255)

    