from django.urls import path
from . import views


urlpatterns = [
    path('add', views.AddLeave.as_view(), name='addLeave')
 ]