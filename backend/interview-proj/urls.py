from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.auth_view, name='auth'),
    path('verify/', views.verify_otp_view, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('problems/', views.problem_list_view, name='problem_list'),
    path('problems/<int:pk>/', views.code_editor_view, name='code_editor'),
    path('behavioral/', views.behavioral_dashboard, name='behavioral_dashboard'),  

]
