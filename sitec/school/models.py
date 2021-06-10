from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
import json

class StudentSitecData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sitec_data')
    panel_data = models.TextField(null=True, blank=True, default=None)
    log_data = models.TextField(null=True, blank=True, default=None)
    reinscription_data = models.TextField(null=True, blank=True, default=None)
    cycle_advance_data = models.TextField(null=True, blank=True, default=None)
    kardex_data = models.TextField(null=True, blank=True, default=None)

    @property
    def owner(self):
        return self.user

    def to_dict(self):
        return {
            'panel_data':   json.loads(self.panel_data),
            'log_data': json.loads(self.log_data),
            'reinscription_data': json.loads(self.reinscription_data),
            'cycle_advance_data': json.loads(self.cycle_advance_data),
            'kardex_data': json.loads(self.kardex_data),        
        }



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

    