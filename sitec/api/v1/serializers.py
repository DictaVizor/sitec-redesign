from school.models import StudentSitecData
from rest_framework import serializers

class StudentSitecDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSitecData
        fields = '__all__'
