from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('login/', views.Userview.as_view()),
    path('otpverify/', views.Otpverify.as_view()),
    path('profile/<int:pk>/', views.UserProfileView.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)