from django.urls import path
from . import views


urlpatterns = [ 
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    path('delete/<int:user_id>', views.DeleteUser.as_view()),
    path('manager/<int:manager_id>', views.ListEmployeesByManager.as_view(),)



]