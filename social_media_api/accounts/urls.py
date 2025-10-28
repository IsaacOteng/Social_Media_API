from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ProfileViewset
# from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:pk>/', ProfileViewset.as_view({'post': 'follow'}), name='follow_user'),
    path('unfollow/<int:pk>/', ProfileViewset.as_view({'delete': 'unfollow'}), name='unfollow_user'),
    path('remove_follow/<int:pk>/', ProfileViewset.as_view({'delete': 'remove_follow'}), name='remove_follow'),
    path('followers/<int:pk>/', ProfileViewset.as_view({'get': 'followers'}), name='profile_followers'),
    path('following/<int:pk>/', ProfileViewset.as_view({'get': 'following'}), name='profile_following'),

]