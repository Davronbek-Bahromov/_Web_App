from django.urls import path
from .views import add_question, QuestionListApiView, update, delete_question, detail_question, AnswerAnyQuestionApiView, AnswerListApiView, update_answer, delete_answer, SeeYourAnswerApiView

urlpatterns = [
    # url for questions
    path('add_question/', add_question,),
    path('get_questions/', QuestionListApiView.as_view(),),
    path('update_question/<int:pk>/', update,),
    path('delete_question/<int:pk>/', delete_question,),
    path('detail_question/<int:pk>/', detail_question,),
    # url for answers
    path('answer_question/<int:question_id>/', AnswerAnyQuestionApiView.as_view(), ),
    path('answer_list/', AnswerListApiView.as_view(), ),
    path('update_answer/<int:pk>/', update_answer, ),
    path('delete_answer/<int:pk>/', delete_answer, ),
    path('get_answer/<int:pk>/', SeeYourAnswerApiView.as_view(), ),

]