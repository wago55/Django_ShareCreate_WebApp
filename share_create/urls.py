from django.urls import path
from .views import (CreateArticleView, DetailArticleView, UpdateArticleView,
                    DeleteArticleView, CreateCommentsView, DeleteCommentsView,
                    FavHomeView, FavDetailView, FollowDetail, FavPageList,
                    )

# app_nameの設定
app_name = 'share_create'

urlpatterns = [
    path('create_article/', CreateArticleView.as_view(), name='create_article'),
    path('detail_article/<int:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('update_article/<int:pk>/', UpdateArticleView.as_view(), name='update_article'),
    path('delete_article/<int:pk>/', DeleteArticleView.as_view(), name='delete_article'),
    path('create_comments/', CreateCommentsView.as_view(), name='create_comments'),
    path('delete_comment/<int:pk>/', DeleteCommentsView.as_view(), name='delete_comment'),
    path('fav_home/<int:pk>/', FavHomeView.as_view(), name='fav_home'),
    path('fav_detail/<int:pk>/', FavDetailView.as_view(), name='fav_detail'),
    path('follow_detail/<int:pk>/', FollowDetail.as_view(), name='follow_detail'),
    path('fav_page_list/', FavPageList.as_view(), name="fav_page_list"),

]
