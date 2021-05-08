import os
from html import escape
from PIL import Image
from ckeditor_uploader import utils
from ckeditor_uploader.utils import storage
from ckeditor_uploader.views import get_upload_filename
from django.core.checks.registry import registry
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import \
    (DetailView, ListView, CreateView, UpdateView, DeleteView)
from mat import settings
from .models import Post, Comment, Category, Likes
from notifications.models import Notification
from users.forms import AddCommentForm, NewPostForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Count
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json

__author__ = "David Khachatryan"
__copyright__ = "Copyright 2021, Mat Ognutyun"
__credits__ = ["Corey Schafer"]
__license__ = "GPL"
__version__ = "2.0.0"
__maintainer__ = "David Khachatryan"
__email__ = "dkhachatryan@wisc.edu"
__status__ = "Production"

def home(request):
    """ Home page view

    Args:
        request (json): type of request made to the backend

    Returns:
        html: main page
    """
    context = {
        'posts': Post.objects.all(),
        'message': 'Գրանցվեք Հարցեր Տալու Համար'
    }
    return render(request, 'blog/home.html', context)

@csrf_exempt
def like_post(request, pk):
    """ Handling the like requests

    Args:
        request (Ajax): Ajax request that sends a like
        pk (int): ID of the post that received the like

    Returns:
        JSON: boolean - liked or not, total_likes - int, total_dislikes - int
    """
    post = get_object_or_404(Post, id=request.POST.get('id'))
    liked = False

    # If the user already liked the post
    if post.likes.filter(id=request.user.id).exists():
        # unlike
        post.likes.remove(request.user)
        liked = False
        Likes.objects.filter(user=request.user, post=post).delete()
    else:
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        post.likes.add(request.user)
        liked = True
        like = Likes.objects.create(user=request.user, post=post)

    context = {
        'post': post,
        'is_liked': liked,
    }

    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html, 
                             'total_likes': post.likes.count(),
                             'total_dislikes': post.dislikes.count(),
                             'liked': liked})


@csrf_exempt
def like_comment(request, pk, pk1):
    """ Handling like requests for a post

    Args:
        request (Ajax):
        pk (int): post_id
        pk1 (int): comment_id

    Returns:
        HttpResponse: boolean - liked/not liked, int - total likes on current comment
    """
    
    comment = get_object_or_404(Comment, id=request.POST.get('id'))
    liked = False

    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    context = {
        'is_liked': liked,
        'total_likes': comment.likes.count()
    }

    if request.method == 'POST':
        return HttpResponse(
            json.dumps(context),
            content_type="application/json")


@csrf_exempt
def dislike_post(request, pk):
    """ This function view handles the dislike logic for a post

    Args:
        request (json): type of request made to the backend
        pk (int): id (primary key) of the post being disliked 
    """
    post = get_object_or_404(Post, id=request.POST.get('id'))
    disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False
    else:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        post.dislikes.add(request.user)
        disliked = True

    if request.is_ajax():
        return JsonResponse({'total_dislikes': post.dislikes.count(),
                             'total_likes': post.likes.count(),
                             'disliked': disliked})


@csrf_exempt
def dislike_comment(request, pk, pk1):
    """ This function handles the dislike logic for a comment

    Args:
        request (json): type of request made to the backend
        pk (int): post id
        pk1 (int): comment id
    """
    comment = get_object_or_404(Comment, id=request.POST.get('id'))
    disliked = False
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        disliked = False
    else:
        comment.dislikes.add(request.user)
        disliked = True

    context = {
        'is_liked': disliked,
        'total_dislikes': comment.dislikes.count()
    }

    if request.method == 'POST':
        return HttpResponse(
            json.dumps(context),
            content_type="application/json")


def CategoryView(request, cats):
    """ List every post in the given category

    Args:
        request (GET): get categories
        cats (Category): given category

    Returns:
        dictionary: posts - all the posts in the given category,
                    cats - given category
                    cat_menu - all the categories
    """

    context = {
        'posts': Post.objects.filter(category=cats.replace('-', ' ')).all(),
        'cats': cats,
        'cat_menu': Category.objects.all()
    }
    return render(request, 'blog/categories.html', context)


def leaderboard(request):
    """ Creeate a leaderboard

    Args:
        request (get): get the leaderboard

    Returns:
        dictionary: leaderboard - top 10 users
    """
    users = User.objects.all()
    lst = []
    for user in users:
        # Don't show the admins
        if user.username == 'PnU2PsbhXEZeP' or user.username == 'lHBziHZm':
            continue
        else:
            karma = count_karma(user) # get post karma
            comment_karma = count_comment_karma(user) # get comment karma
            username = user.username
            lst.append((karma, username, comment_karma))
    # Sort by the following priorities
    # 1) Comment karma
    # 2) post karma
    # 3) username
    lst = sorted(lst, key=lambda tup:(tup[2], tup[0], tup[1]), reverse=True)

    context = {
            'leaderboard': lst[:10]
    }
    return render(request, 'blog/leaderboard.html', context)

def count_karma(user):
    """ Count the total number of likes
        the posts, created by the given user, have

    Args:
        user (User): given user

    Returns:
        int: total likes of the user posts
    """

    karma = 0
    posts = Post.objects.filter(author=user).all()
    for post in posts:
        karma += (int(post.likes.count()) - int(post.dislikes.count()))
            
    return karma

def count_comment_karma(user):
    """ Count the total number of user comment likes

    Args:
        user (User): given user

    Returns:
        int:  total number of user comment likes
    """

    karma = 0
    comments = Comment.objects.filter(name=user).all()
    for comment in comments:
        karma += comment.likes.count()

    return karma   

def DeleteNotification(request, pk):
    """ 

    Args:
        request (post): Delete a notification
        pk (int): id of the notification

    Returns:
        HttpResponseDirect: directs to the html page of the post
                            that rendered the notification
    """
    try:
        # List the notification as seen
        notif = Notification.objects.get(id=pk)
        notif.delete()
        
    except:
        return HttpResponseRedirect(reverse('blog-home'))

    return HttpResponseRedirect(reverse('post-detail', args=[str(notif.post.id)]))


def BestPosts(request):
    """ Return the best posts

    Args:
        request (get): get best posts

    Returns:
        dictionary: containing the best posts sorted
    """
 
    context = {
        # Sort by count
        'posts': Post.objects.annotate(count=Count('likes')).order_by('-count')
    }
    return render(request, 'blog/best_posts.html', context=context)


class PostListView(ListView):
    """ Main view - AKA the home view

    Args:
        ListView

    Returns:
        dictionary: cat_menu 
    """

    model = Post # list posts
    template_name = 'blog/home.html' # list the home template
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5 # number of posts on each page

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()

        try:
            notifications = Notification.objects.filter(user=self.request.user).all()

            not_counter = 0
            for notification in notifications:
                if not notification.is_seen and notification.user != notification.sender:
                    not_counter += 1
        except:
            notification = []
            context = super(PostListView, self).get_context_data(*args, **kwargs)
            context["cat_menu"] = cat_menu
            return context

        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["notifications"] = notifications
        context["not_counter"] = not_counter
        return context


class UserPostListView(ListView):
    """ List the posts created by the given user """

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        """ Return a list of posts made by the given user """

        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UserPostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class PostDetailView(DetailView):
    """[summary]

    Args:
        DetailView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Post

    def get_context_data(self, *args, **kwargs):
        """[summary]

        Returns:
            [type]: [description]
        """
        cat_menu = Category.objects.all()

        try:
            notifications = Notification.objects.filter(user=self.request.user).all()

            not_counter = 0
            for notification in notifications:
                if not notification.is_seen and notification.user != notification.sender:
                    not_counter += 1
        except TypeError:
            notification = []
            context = super(PostDetailView, self).get_context_data(*args, **kwargs)
            context["cat_menu"] = cat_menu
            return context

        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["notifications"] = notifications
        context["not_counter"] = not_counter
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """[summary]

    Args:
        LoginRequiredMixin ([type]): [description]
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Post
    
    form_class = NewPostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        """[summary]

        Args:
            form ([type]): [description]

        Returns:
            [type]: [description]
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """This is a test on whether a user can access this file

        Returns:
            boolean: true if the user requesting this view
                     is the author of the given comment
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """[summary]

    Args:
        LoginRequiredMixin ([type]): [description]
        UserPassesTestMixin ([type]): [description]
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """This is a test on whether a user can access this file

        Returns:
            boolean: true if the user requesting this view
                     is the author of the given comment
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """[summary]

    Args:
        LoginRequiredMixin ([type]): [description]
        UserPassesTestMixin ([type]): [description]
        DeleteView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Post
    success_url = '/'

    def test_func(self):
        """ This is a test on whether a user can access this file

        Returns:
            boolean: true if the user requesting this view
                     is the author of the given comment
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentCreateView(LoginRequiredMixin, CreateView):
    """[summary]

    Args:
        LoginRequiredMixin ([type]): [description]
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Comment
    template_name = 'blog/add_comment.html'
    form_class = AddCommentForm

    def form_valid(self, form):
        """[summary]

        Args:
            form ([type]): [description]

        Returns:
            [type]: [description]
        """
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """[summary]

    Args:
        LoginRequiredMixin ([type]): [description]
        UserPassesTestMixin ([type]): [description]
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = Comment
    template_name = 'blog/update_comment.html'

    form_class = AddCommentForm

    def form_valid(self, form):
        """[summary]

        Args:
            form ([type]): [description]

        Returns:
            [type]: [description]
        """
        form.instance.name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """ This is a test on whether a user can access this file

        Returns:
            boolean: true if the user requesting this view
                     is the author of the given comment
        """

        comment = self.get_object()
        return self.request.user == comment.name


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete the given comment

    Args:
        LoginRequiredMixin (): require login
        UserPassesTestMixin (): require the user to pass the test
        DeleteView (): 
    """
    model = Comment

    def get_success_url(self, **kwargs):
        # Where does it redirect after deleting the comment
        return self.object.get_absolute_url()

    def test_func(self):
        """ This is a test on whether a user can access this file

        Returns:
            boolean: true if the user requesting this view
                     is the author of the given comment
        """
        
        comment = self.get_object()
        return self.request.user == comment.name


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