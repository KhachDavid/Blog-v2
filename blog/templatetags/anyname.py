from django import template
from blog.models import Post
from users.models import Profile
from django.contrib.auth.models import User

__author__ = "David Khachatryan"
__copyright__ = "Copyright 2021, Mat Ognutyun"
__credits__ = None
__license__ = "GPL"
__version__ = "2.0.0"
__maintainer__ = "David Khachatryan"
__email__ = "dkhachatryan@wisc.edu"
__status__ = "Production"

register = template.Library()


@register.filter
def get_client_name(pk, attr):
    """[summary]

    Args:
        pk ([type]): [description]
        attr ([type]): [description]

    Returns:
        [type]: [description]
    """
    obj = getattr(Post.objects.get(id=pk), attr)
    return obj


@register.filter
def get_post_author_profile_img_url(pk, attr):
    """[summary]

    Args:
        pk ([type]): [description]
        attr ([type]): [description]

    Returns:
        [type]: [description]
    """
    obj = getattr(Post.objects.get(id=pk).author.profile.image, attr)
    return obj


@register.filter
def get_post_comments(pk, attr):
    """[summary]

    Args:
        pk ([type]): [description]
        attr ([type]): [description]

    Returns:
        [type]: [description]
    """
    obj = int(getattr(Post.objects.get(id=pk).comments.count, attr))
    # {{ view.kwargs.pk|get_post_comments:'count' }}
    return obj


@register.filter
def get_user_author_profile_img(user1, attr):
    """[summary]

    Args:
        user1 ([type]): [description]
        attr ([type]): [description]

    Returns:
        [type]: [description]
    """
    us = User.objects.filter(username=user1).first()
    profile = Profile.objects.filter(user=us).first()
    obj = getattr(profile.image, attr)
    return obj


@register.filter
def get_content_preview(pk):
    """[summary]

    Args:
        pk ([type]): [description]

    Returns:
        [type]: [description]
    """
    obj = Post.objects.get(id=pk).content
    obj = get_p_content(obj)

    if len(obj) > 101:
        retVal = obj[:100] 
        return retVal
    else:
        retVal = obj
        return retVal


def get_p_content(obj):
    """[summary]

    Args:
        obj ([type]): [description]

    Returns:
        [type]: [description]
    """
    try:
        obj = str(obj)
        attempt = obj
        ret_value = ""
        index = 0
        for char in attempt:
            if index == 188:
                print(1)
            char_p_index = 0
            if char == 'i':
                if index != 0 and obj[index - 1] == '<':
                    if index != int(len(attempt)) - 1 and obj[index + 1] == 'm':
                        if index != int(len(attempt)) - 2 and obj[index + 2] == 'g':
                            while(obj[index + char_p_index] != '>'):
                                char_p_index += 1
                            ret_value += obj[0:index - 1] 
                            ret_value += obj[char_p_index + index + 1:]
                            return ret_value
            index += 1   

        return obj
    
    except:
        return obj

def check_for_closing_tags(retVal, obj):
    """[summary]

    Args:
        retVal ([type]): [description]
        obj ([type]): [description]
    """
    smaller_index = 0
    slash_index = 0
    check_val = retVal
    index = int(len(check_val)) - 1
    try:
        while check_val[index] != '<':
            print(1)
            index -= 1
            if index == 0:
                break
            elif check_val[index] == '<' and smaller_index == 0:
                smaller_index = index
            elif check_val[index] == '/' and slash_index == 0:
                slash_index = index
            if slash_index != 0 and smaller_index != 0:
                if smaller_index > slash_index:
                    while obj[smaller_index] != '>':
                        smaller_index += 1
                return obj[:smaller_index]
    except:
        return obj[:30]

@register.filter
def subtract(num1, num2):
    """ Subtract two numbers """
    return int(num1) - int(num2)


@register.filter
def check_if_user_liked(user, post):
    """ Return true if the given user liked
        the given post

    Args:
        user (USER): An instance of the model user
        post (POST): An instance of the model post
    """
    return post.likes.filter(id=user.id).exists()


@register.filter
def check_if_user_disliked(user, post):
    """ Return true if the given user disliked
        the given post

    Args:
        user (USER): An instance of the model user
        post (POST): An instance of the model post
    """
    return post.dislikes.filter(id=user.id).exists() 