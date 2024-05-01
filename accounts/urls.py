from django.urls import path
from .views import RegistrationApiView

urlpatterns = [
    path('register/', RegistrationApiView.as_view(), ),
    
]