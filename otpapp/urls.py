from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf.urls import url

urlpatterns = [
    path('login/', views.Userview.as_view()),
    path('otpverify/', views.Otpverify.as_view()),
    path('profile/<int:pk>/', views.UserProfileView.as_view()),
    url(r'^user/upload', views.UserFileView.as_view(), name='UserFileView'),


]

urlpatterns = format_suffix_patterns(urlpatterns)