import rest_framework
from rest_registration.api.views import login as rest_login
from rest_framework.decorators import api_view, permission_classes
from rest_registration.exceptions import UserNotFound
from sitec_api.models import SitecApi   
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwner
from django.contrib.auth.models import User

@api_view(['POST'])
def sync_sitec(request):
    api = SitecApi()
    response = api.login(**request.data)

    if response.status_code != 200:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    data = api.retrieve_all_data()

    user = None
    try:
        user = User.objecs.get(username=request.data['username'])
    except Exception:
        pass

    if not user:
        user = User.objects.create_user(request.data['username'], password=request.data['password'])

    return Response(status=status.HTTP_200_OK, data=data)