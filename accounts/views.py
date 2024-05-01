from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from user_profile.models import UserProfile

# Create your views here.
class RegistrationApiView(APIView):
    def post(self, request):
        username= request.data['username']
        password = request.data['password']
        email = request.data['email']
        phone = request.data['phone']

        user = User(username=username, email=email,)
        user.set_password(password)

        user.save()
        UserProfile.objects.create(name=user, phone=phone)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'status': 'success',
                'user_id': user.id,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        )