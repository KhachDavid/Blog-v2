from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save, post_delete

from notifications.models import Notification
from .utils import strip_tags

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    category = models.CharField(max_length=100, default='Առանց Կատեգորիա')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_comments')

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name.username)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = strip_tags(comment.body[:90])
        sender = comment.name

        notify = Notification(post=post, sender=sender, user=post.author, text_preview=text_preview, notification_type=2)
        notify.save()

    def user_del_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.name

        notify = Notification.objects.filter(post=post, user=post.author, sender=sender, notification_type=2)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        if len(post.title) > 40:
            notify = Notification(post=post, sender=sender, user=post.author, notification_type=1, text_preview=post.title[:40] + "...")
            notify.save()
        else:
            notify = Notification(post=post, sender=sender, user=post.author, notification_type=1, text_preview=post.title)
            notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user

        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()

    def __str__(self):
        return str(self.user)


#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender = Likes)

#Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)

