from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import (SignupView, HomeView, UpdateProfileView, ListProfileView,
                    InquiryView, DetailProfileView, FollowList, FollowerList,
                    FollowListDetail, FollowerListDetail)

# app_nameの指定
app_name = 'accounts'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('list_profile/', ListProfileView.as_view(), name='list_profile'),
    path('inquiry_form/', InquiryView.as_view(), name='inquiry'),
    path('detail_profile/<int:pk>/', DetailProfileView.as_view(), name="detail_profile"),
    path('follow_list/', FollowList.as_view(), name="follow_list"),
    path('follower_list/', FollowerList.as_view(), name='follower_list'),
    path('follow_list_detail/<int:pk>/', FollowListDetail.as_view(), name='follow_list_detail'),
    path('follower_list_detail/<int:pk>/', FollowerListDetail.as_view(), name='follower_list_detail'),
]