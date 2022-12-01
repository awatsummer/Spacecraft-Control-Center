from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader

from .models import FlightOperator

def index(request):

    if request.user.is_authenticated:
        return redirect('fo:home')
    else:
        return redirect('fo:login')

def foRegister(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            ######################### mail system ####################################
            send_mail(
                'STaTE Registration',
                'Thank you for registering to STaTE!',
                None,
                [email],
                fail_silently=False,
            )
            ##################################################################
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            FlightOperator.objects.create(user = user)
            return redirect('fo:home')
    else:
        form = UserRegisterForm()

    return render(request, 'fo/foRegister.html', {'form': form, 'title':'register here'})

def foLogin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None and user.is_staff:
            return redirect('tclogin')
        if user is not None and not user.is_staff:
            form = login(request, user)
            return redirect('fo:home')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated:
        return redirect('fo:home')

    form = AuthenticationForm()
    return render(request, 'fo/foLogin.html', {'form':form, 'title':'log in'})

def foLogout(request):
    logout(request)
    return redirect('fo:login')

def foHome(request):
    flightOperator = get_object_or_404(FlightOperator, user = request.user)
    return render(request, 'fo/foHome.html', {'flightOperator':flightOperator})