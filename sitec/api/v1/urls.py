from rest_framework import routers
from rest_registration.api.urls import login, logout, profile
from django.urls import path, include
from .views import sync_sitec, StudentSitecDataViewSet

router = routers.DefaultRouter()
router.register('students-sitec-data', StudentSitecDataViewSet)

app_name = 'api-v1'
urlpatterns = router.urls

urlpatterns += [
    path('accounts/login', login, name='login'),
    path('accounts/logout', logout, name='logout'),
    path('accounts/profile', profile, name='profile'),
    path('sync-sitec', sync_sitec, name='sync-sitec')
]