from django.urls import path
from .views import tasklist,taskdetail, taskcreate,taskupdate,taskdelete,userlogin,useregister
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('login/',userlogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',useregister.as_view(),name='register'),

    path('',tasklist.as_view(),name='tasks'),
    path('task/<int:pk>/', taskdetail.as_view(),name='task'),
    path('newtask/',taskcreate.as_view(),name='newtask'),
    path('task/<int:pk>/update/',taskupdate.as_view(),name='updatetask'),
    path('task/<int:pk>/delete/',taskdelete.as_view(),name='deletetask'),

]
