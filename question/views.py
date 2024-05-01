from django.shortcuts import render
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

# views for questions 

# add any question
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request):
    user = request.user
    post_data = request.data
    
    try:
        serializer = QuestionSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# see every question
class QuestionListApiView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
# update question
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update(request, pk):
    
    try:
        question = Question.objects.get(pk=pk, created_by=request.user)
    
    except Question.DoesNotExist:
        return Response({"error": "Question Not Found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionSerializer(question, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
# delete question
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_question(request, pk):
    
    try:
        question = Question.objects.get(pk=pk, created_by=request.user)
    
    except Question.DoesNotExist:
        return Response({"error": "Question Not Found"}, status=status.HTTP_404_NOT_FOUND)

    question.delete()

    return Response({"message":"Question Successfully Deleted.!"})

# detail question
@api_view(['GET'])
def detail_question(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    
    except Question.DoesNotExist:
        return Response({"error":"Question Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = QuestionSerializer(question)

    return Response(serializer.data)

# views for answer "|"

# answer any question

class AnswerAnyQuestionApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, question_id):
        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=request.user, question_id=question_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# see all answers 
class AnswerListApiView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_answer(request, pk):
    try:
        answer = Answer.objects.get(id=pk, created_by=request.user)
        
    except Answer.DoesNotExist:
        return Response({'error':'Answer Not Found.!'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AnswerSerializer(answer, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete answer
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_answer(request, pk):
    try:
        answer = Answer.objects.get(id=pk, created_by=request.user)
        answer.delete()
        return Response({'message': 'answer successfully deleted.!'})
    except Answer.DoesNotExist:
        return Response({'error': 'Answer Not Found.!'}, status=status.HTTP_404_NOT_FOUND)

# see detail your answer     
class SeeYourAnswerApiView(APIView):
    def get(self, request, pk):
        try:
            answer = Answer.objects.get(id=pk)
        except Answer.DoesNotExist:
            return Response({'error': 'Answer Not Found.!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnswerSerializer(answer)
        
        return Response(serializer.data)