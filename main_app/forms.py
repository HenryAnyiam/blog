from django import forms
from django.contrib.auth.models import User
from .models import Post


class UserCreateForm(forms.ModelForm):
    """form to handle user creation"""

    class Meta:

        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password']


class PostCreateForm(forms.ModelForm):
    """form to handle Post creation"""

    published_date = forms.DateTimeField(required=False)

    class Meta:

        model = Post
        exclude = ["title", "content"]
