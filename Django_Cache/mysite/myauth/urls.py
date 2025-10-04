from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    AboutMeView,
    NewLogoutView,
    RegisterView,
    UserUpdateAvatarView,
    UsersListView,
    AboutUserView,
)

app_name = "myauth"

urlpatterns = [
    path('login/',
         LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
    ),
         name='login'),
    path('logout/', NewLogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),

    path("users/", UsersListView.as_view(), name="list_users"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("about-user/<int:pk>/", AboutUserView.as_view(), name="user_details"),

    path("new_avatar/<int:pk>/", UserUpdateAvatarView.as_view(), name="new_avatar"),
]
