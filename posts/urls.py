from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostCreateView,
    PostDeleteView,
    ProfileView,
    ResponseListView,
    ResponseDeleteView,
    ResponseUpdateView,
)


urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('response_list/<int:pk>', ResponseListView.as_view(), name='response_list'),
    path('response_list/<int:pk>/delete/',
         ResponseDeleteView.as_view(), name='response_delete'),
    path('response_list/<int:pk>/update/',
         ResponseUpdateView.as_view(), name='response_update'),
]
