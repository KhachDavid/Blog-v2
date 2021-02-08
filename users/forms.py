from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from blog.models import Comment, Post, Category
from ckeditor_uploader.fields import RichTextUploadingField

# categories = [('Math', 'Math'), ('Coding', 'Coding')]
categories = []
for category in Category.objects.all():
    categories.append((category, category))

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

        widgets = {
            'body': RichTextUploadingField(blank=True, null=True)
        }


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': RichTextUploadingField(blank=True, null=True),
            'category': forms.Select(choices=categories, attrs={'class': 'form-control'})
        }
        
