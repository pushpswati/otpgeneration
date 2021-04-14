from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.Userview.as_view()),
    path('otpverify/', views.Otpverify.as_view()),
    path('profile/<int:pk>/', views.UserProfileView.as_view()),
    url(r'^user/upload', views.UserFileView.as_view(), name='UserFileView'),
    url(r'^user/jobsdetails', views.JobDetailsView.as_view(), name='JobDetailsView'),
    


]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
       urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)