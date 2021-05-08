from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


def register(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')

            email = form.cleaned_data.get('email')
            emails = User.objects.filter(email=email).first()
            username11 = User.objects.filter(username=username).first()
            if isinstance(emails, type(None)):
                messages.success(request, f'{username}, ձեր հաշիվը ստեղծված է։ Դուք կարող եք մուտք գործել!')
                form.save()
                return redirect('login')
            args = {}
            email_error_message = "Այս Էլեկտրոնային հասցեն զբաղված է"

            if form.cleaned_data.get('password1') != form.cleaned_data.get('password2'):
                args['password_error_message'] = 'Գաղտնաբառերը չեն համընկնում'

            if not isinstance(emails, type(None)):
                args['email_error_message'] = email_error_message

            if not isinstance(username11, type(None)):
                args['username_error_message'] = f'{username} ծածկանունը զբաղված է'

            form = UserRegisterForm()
            args['form'] = form
            messages.warning(request, f'{email}, էլեկտրոնային հասցեն զբաղված է!')
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)