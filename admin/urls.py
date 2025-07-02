from . import views
from django.urls import path
app_name = 'admin'

urlpatterns = [
    path('account/', views.account_view, name='account'),
    path('permission/', views.permission_view, name='permission'),
    path('list_of_account/', views.list_of_account_view, name='list_of_account'),

]