from . import views
from django.urls import path
app_name = 'student'

urlpatterns = [
    path('learning/', views.learning_view, name='learning'),
    path('ide/', views.ide_view, name='ide'),
    path('practice/', views.practice_view, name='practice'),
    path('quizAI/', views.quizAI_view, name='quizAI'),
]