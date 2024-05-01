from django.shortcuts import render
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Post, Comment, Channel
from rest_framework.generics import ListAPIView 
from .serializers import PostSerializer, CommentSerializer, ChannelSerializer, ReadOnlyPostSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.response import Response

# share post not yet...

# views for channel model
# create_channel
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_channel(request):
    created_by = request.user
    
    try:
        serializer = ChannelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=created_by)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(str(e))
    
class ListChannelApiView(ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

# detail Channel
@api_view(['GET'])
def get_channel(request, pk):
    try:
        channel = Channel.objects.get(pk=pk)
        posts = Post.objects.filter(channel=channel)
        seralizer = ChannelSerializer(channel)
        seralizers = PostSerializer(posts, many=True)
        return Response({
            "channel": seralizer.data,
            "posts": seralizers.data,
        })
    except Channel.DoesNotExist:
        return Response({"message":"Channel Not Found.!"}, status.HTTP_404_NOT_FOUND)
    
# delete channel
# channel
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_channel(request, pk):
    try:
        channel = Channel.objects.get(pk=pk, user=request.user)
    
    except Channel.DoesNotExist:   
        return Response({"message":"Channel Not Found.!"}, status=status.HTTP_404_NOT_FOUND)
    
    channel.delete() 
    
    return Response({"message":"Channel Successfully Deleted.!"})


# create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_api_view(request):
    user = request.user
    post_data = request.data

    try:
        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# show list and search posts for title and body. This searching code not yet over.
class PostListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = ReadOnlyPostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['id', 'title', 'body']
    search_fields = ['title', 'body']
    
# get your posts
@cache_page(60 * 10)  # Cache the response for 10 minutes
@api_view(['GET'])
def get_post(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(created_by=request.user)

        if posts:
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "You have not any posts...!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "User is not authenticated.!"}, status=status.HTTP_401_UNAUTHORIZED)

    # Explicitly return an empty Response if no conditions are met
    return Response(status=status.HTTP_204_NO_CONTENT)

# update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)

    except Post.DoesNotExist:
        return Response({"error":"Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete_post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)
        post.delete()
        return Response({"message":"Post Succesfully Deleted.!"})
    
    except Post.DoesNotExist:
        return Response({"message":"Post Succesfully Deleted.!"}, status=status.HTTP_404_NOT_FOUND)

# views for comment 
class CreateCommentApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        seralizer = CommentSerializer(data=request.data)
        if seralizer.is_valid():
            try:
                post = Post.objects.get(pk=pk)
                seralizer.save(created_by=request.user, post=post)
                return Response(seralizer.data, status=status.HTTP_201_CREATED)
            except Post.DoesNotExist:
                return Response({'error':'Post not found.!'}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as i:
                return Response({'error':str([i])})
        else:
            return Response(seralizer.errors, status=status.HTTP_404_NOT_FOUND)
        
# comment list
class CommentListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cache_page(60 * 15)(view)

# update comment
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, created_by=request.user)
    except Comment.DoesNotExist:
        return Response({'error':'Comment Not Found.!'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(comment, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete comment
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, created_by=request.user)
    except Comment.DoesNotExist:
        return Response({'error':'Comment Not Found.!'}, status=status.HTTP_404_NOT_FOUND)
    
    comment.delete()

    return Response({'message':'Comment Successfully Deleted.!'}, status=status.HTTP_200_OK)

# like and dislike for posts

class LikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.add(request.user)
        post.dislike.remove(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

class DislikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.remove(request.user)
        post.dislike.add(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentLikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.add(request.user)
        post.dislike.remove(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDislikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.remove(request.user)
        post.dislike.add(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)