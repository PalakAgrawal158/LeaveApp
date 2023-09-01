from django.urls import path
from . import views


urlpatterns = [
    path('add', views.AddLeave.as_view(), name='addLeave'),
    path('list', views.ViewPendingLeaves.as_view(), name="listLeaves"),
    path('update', views.ApproveRejectLeave.as_view(), name="ApproveLeave"),
    path('view', views.ViewEmployeeLeaves.as_view(), name="ViewEmployeeLeaves"),
    path('delete/<int:leave_id>', views.DeleteLeave.as_view(), name="DeleteLeave"),

 ]