from django.urls import path
from user_auth.views import (
                                CreateUser,
                                UserRetrieveUpdateView,
                                ResetPassword,
                                UserListAPIView,
                                LogoutView
                            )

urlpatterns = [
    path('users',CreateUser.as_view()),
    path('users-list',UserListAPIView.as_view()),
    path('users/<int:pk>',UserRetrieveUpdateView.as_view()),
    path('users/reset-password/<int:pk>',ResetPassword.as_view()),
    path('logout',LogoutView.as_view()),

]
