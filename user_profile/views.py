from .models import UserProfile
from django.shortcuts import render
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status

# List user_profiles
class GetUserProfile(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# update user_profile
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, pk):
    try:
        user_profile = UserProfile.objects.get(pk=pk, user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'error':'User Profile Not Found.!'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)