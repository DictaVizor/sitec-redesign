from school.models import StudentSitecData
from rest_framework import serializers
from rest_registration.api.serializers import DefaultUserProfileSerializer

class StudentSitecDataSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return instance.to_dict()

    class Meta:
        model = StudentSitecData
        fields = '__all__'
        read_only_fields = ['user']

class UserProfileSerializer(DefaultUserProfileSerializer):
    sitec_data = StudentSitecDataSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields = ('username', 'first_name', 'last_name', 'sitec_data')
    
