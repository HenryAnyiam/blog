from django.shortcuts import render
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from django.views.generic import TemplateView, FormView, UpdateView, View
from .models import Post
from .forms import UserCreateForm, PostCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.
class UserCreateView(TemplateView):
    """create a new user"""

    template_name = "signup.html"

    def get(self, request):
        """get signup page"""

        return render(request, self.template_name)

    def post(self, request):
        """signup a new user"""

        form = UserCreateForm(request.POST)

        if form.is_valid():
            new_user = User.objects.create_user(
                            first_name=request.POST.get('first_name').title(),
                            last_name=request.POST.get('last_name').title(),
                            email=request.POST.get('email'),
                            username=request.POST.get('username').lower(),
                            password=request.POST.get('password'))
            user = authenticate(request,
                                username=request.POST.get('username').lower(),
                                password=request.POST.get('password'))
            login(request, user)
            return HttpResponseRedirect(reverse("main_app:home"))
        else:
            return render(request, self.template_name, {"error": form.errors})


class UserLoginView(LoginView):
    """login a user"""

    template_name = "login.html"

    def get_success_url(self):
        """redirect upon successful creation"""
        return reverse("main_app:home")


class UserLogoutView(LogoutView):
    """logout a user"""

    def get_success_url(self):
        """redirect upon successful creation"""
        return reverse("main_app:home")

class PostCreateView(LoginRequiredMixin, FormView):
    """create a new Post"""

    login_url = "/auth/login"
    template_name = "new_post.html"
    model = Post

    def get(self, request):
        """get new post page"""

        return render(request, self.template_name)

    def post(self, request):
        """create new post"""

        form = PostCreateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            author = User.objects.get(id=request.POST.get("author"))
            post = Post.objects.create(title=request.POST.get("title"),
                    content=request.POST.get("content"),
                    author=author)

            return HttpResponseRedirect(reverse("main_app:home"))
        else:
            return render(request, self.template_name, {"error": form.errors})



class PostUpdateView(LoginRequiredMixin, UpdateView):

    model = Post
    login_url = "/auth/login"
    template_name = "edit_post.html"
    fields = ["title", "content"]

    def get_success_url(self):
        """redirect upon successful creation"""
        return reverse("main_app:home")


class PostListView(ListView):
    """view to view all posts"""

    model = Post
    context_object_name = "posts"
    template_name = "home.html"
    queryet = Post.objects.order_by("-published_date")


class PostDetailView(DetailView):
    """view to view a particular post"""

    model = Post
    context_object_name = "post"
    template_name = "post.html"

    def get_success_url(self):
        """redirect upon successful creation"""
        return reverse("main_app:home")


class PostDeleteView(View):
    """delete a post"""

    login_url = "/auth/login"

    def delete(self, request, pk):
        """delete post"""

        post = Post.objects.get(id=pk);
        post.delete()

        return HttpResponseRedirect(reverse("main_app:home"))
