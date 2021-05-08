from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification

def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    context = {
        'notifications': notifications
    }

    return render(request, 'blog/notifications.html', context)
