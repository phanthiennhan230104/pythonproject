from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('student_homepage/', views.student_homepage, name='student_homepage'),
    path('teacher_homepage/', views.teacher_homepage, name='teacher_homepage'),
    path('admin_homepage/', views.admin_homepage, name='admin_homepage'),

]
