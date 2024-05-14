from django.urls import path
from .views import PostListView, PostDetailView, PostDeleteView, UserLoginView
from .views import UserCreateView, PostCreateView, PostUpdateView, UserLogoutView

app_name = "main_app"

urlpatterns = [
    path("user", UserCreateView.as_view(), name="signup"),
    path("auth/login", UserLoginView.as_view(), name="login"),
    path("auth/logout", UserLogoutView.as_view(), name="logout"),
    path("", PostListView.as_view(), name="home"),
    path("post", PostCreateView.as_view(), name="new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="delete")
]
