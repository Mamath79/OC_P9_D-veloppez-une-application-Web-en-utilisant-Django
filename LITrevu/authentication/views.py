from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # associer le nouvel user au group CREATORS
            creators_grp = Group.objects.get(name='creators') 
            creators_grp.user_set.add(user)
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

