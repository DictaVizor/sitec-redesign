from rest_framework.permissions import IsAuthenticated
from school.models import StudentSitecData
import rest_framework
from rest_registration.api.views.login import perform_login
from rest_framework.decorators import api_view, permission_classes
from rest_registration.exceptions import UserNotFound
from sitec_api.models import SitecApi   
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner
from .serializers import StudentSitecDataSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
import json
from sitec_api.utils import clean_spanish_characters

@api_view(['POST'])
def sync_sitec(request):
    api = SitecApi()
    response = api.login(**request.data)

    if response.status_code != 200:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = api.retrieve_all_data()
    for key,value in data.items():
        data[key] = clean_spanish_characters(json.dumps(value))

    user = None
    try:
        user = User.objects.get(username=request.data['username'])
    except Exception:
        pass

    if not user:
        user = User.objects.create_user(request.data['username'], password=request.data['password'])
    
    student_sitec_data, created = StudentSitecData.objects.get_or_create(user=user)
    student_sitec_data_serializer = StudentSitecDataSerializer(student_sitec_data, data=data, partial=True)
    student_sitec_data_serializer.is_valid(raise_exception=True)
    student_sitec_data_serializer.save()

    perform_login(request._request, user)

    return Response(status=status.HTTP_200_OK, data=student_sitec_data_serializer.data)


class StudentSitecDataViewSet(viewsets.ModelViewSet):
    queryset = StudentSitecData.objects.all()
    serializer_class = StudentSitecDataSerializer
    permission_classes = [IsOwner|IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)