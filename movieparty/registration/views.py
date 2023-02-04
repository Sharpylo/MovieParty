from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import RegisterForm


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return HttpResponseRedirect('/')

    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})
