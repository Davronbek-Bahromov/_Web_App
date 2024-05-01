from django.urls import path
from .views import GetUserProfile

urlpatterns = [
    path('get_user_profile/', GetUserProfile.as_view(), ),
]