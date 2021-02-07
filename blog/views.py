import os
from html import escape

from PIL import Image
from ckeditor_uploader import utils
from ckeditor_uploader.utils import storage
from ckeditor_uploader.views import get_upload_filename
from django.core.checks.registry import registry
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import \
    (DetailView, ListView, CreateView, UpdateView, DeleteView)

from mat import settings
from .models import Post, Comment, Category
from users.forms import AddCommentForm, NewPostForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django import forms
from ckeditor_uploader.fields import RichTextUploadingField



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


def CommentLikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(Comment.objects.filter(id=pk).first().post.id)]))


def CategoryView(request, cats):
    context = {
        'posts': Post.objects.filter(category=cats.replace('-', ' ')).all(),
        'cats': cats,
        'cat_menu': Category.objects.all()
    }
    return render(request, 'blog/categories.html', context)


def leaderboard(request):
    users = User.objects.all()
    lst = []
    for user in users:
        karma = count_karma(user)
        comment_karma = count_comment_karma(user)
        username = user.username
        lst.append((karma, username, comment_karma))
    lst.sort()
    lst.reverse()

    context = {
        'leaderboard': lst
    }
    return render(request, 'blog/leaderboard.html', context)

def count_karma(user):
    karma = 0
    posts = Post.objects.filter(author=user).all()
    for post in posts:
        karma += post.likes.count()
            
    return karma

def count_comment_karma(user):
    karma = 0
    comments = Comment.objects.filter(name=user).all()
    for comment in comments:
        karma += comment.likes.count()

    return karma


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UserPostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    
    form_class = NewPostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/add_comment.html'
    form_class = AddCommentForm

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/update_comment.html'

    form_class = AddCommentForm

    def form_valid(self, form):
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.name:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.name:
            return True
        return False


def handler400(request, exception):
    return render(request, 'users/400.html', status=400)


def handler403(request, exception):
    return render(request, 'users/403.html', status=403)


def handler404(request, exception):
    return render(request, 'users/404.html', status=404)


def handler500(request):
    return render(request, 'users/500.html', status=500)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})