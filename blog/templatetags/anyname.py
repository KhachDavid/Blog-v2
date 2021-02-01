from django import template
from blog.models import Post

register = template.Library()


@register.filter
def get_client_name(pk, attr):
    obj = getattr(Post.objects.get(id=pk), attr)
    return obj


@register.filter
def get_post_author_profile_img_url(pk, attr):
    obj = getattr(Post.objects.get(id=pk).author.profile.image, attr)
    return obj


@register.filter
def get_post_comments(pk, attr):
    obj = int(getattr(Post.objects.get(id=pk).comments.count, attr))
    # {{ view.kwargs.pk|get_post_comments:'count' }}
    return obj

