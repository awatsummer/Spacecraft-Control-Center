import numpy
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

from .models import TestConductor, Sim, Subsystem, Class
from .forms import UserRegisterForm, SimCreationForm, ClassForm
from fo.forms import SubsystemForm

###############################################################################
def index(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('tc:home')
    else:
        return redirect('tc:login')
  
###############################################################################
def tcRegister(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # Send registration confirmation
            send_mail(
                'STaTE Registration',
                'Thank you for registering to STaTE!',
                None,
                [email],
                fail_silently=False,
            )
            user = authenticate(request, username = username, password = password)
            form = login(request, user)
            TestConductor.objects.create(user = user)
            user.is_staff=True
            #user.is_superuser=True
            user.save();
            return redirect('tc:home')
    else:
        form = UserRegisterForm()

    return render(request, 'tc/register.html', {'form': form, 'title':'register here'})
  
###############################################################################
def tcLogin(request):      

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None and not user.is_staff:
            return redirect('fo:login')
        if user is not None and user.is_staff:
            form = login(request, user)
            return redirect('tc:home')
        else:
            messages.info(request, f'account does not exist')

    elif request.user.is_authenticated and request.user.is_staff:
        return redirect('tc:home')

    form = AuthenticationForm()
    return render(request, 'tc/login.html', {'form':form, 'title':'log in'})

###############################################################################
def tcLogout(request):
    logout(request)
    return redirect('tc:login')

###############################################################################
def tcHome(request):
    classes = Class.objects.all()

    return render(request, 'tc/tcHome.html', {"classes":classes})
  
###############################################################################
<<<<<<< Updated upstream
def classHome(request, class_name):
    classobj = Class.objects.get(class_name = class_name)
    sims = classobj.sims.all()
    return render(request, 'tc/classHome.html', {"sims": sims, "class_name": classobj})
=======
def classHome(request, k):

    group = Group.objects.all().filter(name=k).values_list('sim_list', flat=True)
    data = numpy.asarray(group)
    print(data)
    if (data[0]!=None):
        sims = ['']*(len(data))
        for e in range(len(data)):
            print(Sim.objects.get(pk=data[e]))
            sims[e] = Sim.objects.get(pk=data[e])
        print(sims)
    else:
        sims=[]
    return render(request, 'tc/classHome.html', {"sims":sims})
>>>>>>> Stashed changes

###############################################################################
def getGroups(request):
    
    group = list(request.user.groups.values_list('name', flat = True))
    data = numpy.asarray(group)
    print(data) 
    return render(request, 'tc: home.html', {"data":data})

###############################################################################
def createSim(request, class_name):
    
    if request.method == 'POST':
        form = SimCreationForm(request.POST)
        
        if form.is_valid():
            sim_name = form.cleaned_data.get('sim_name')
            sys1_name = form.cleaned_data.get('sys1_name')
            sys2_name = form.cleaned_data.get('sys2_name')
            sys3_name = form.cleaned_data.get('sys3_name')
            flight_operators = form.cleaned_data.get('flight_operators')
            class_belong = form.cleaned_data.get('class_belong')

            sim = Sim.objects.create(sim_name = sim_name)
            subsystem1 = Subsystem.objects.create(sys_name = sys1_name)
            subsystem2 = Subsystem.objects.create(sys_name = sys2_name)
            subsystem3 = Subsystem.objects.create(sys_name = sys3_name)

            sim.sys_list.add(subsystem1, subsystem2, subsystem3)
<<<<<<< Updated upstream

=======
            for class_belong in class_belong:
                sim.class_belong.add(class_belong)
                class_belong.sim_list.add(sim)
            form.save_m2m()
            ##gohere
>>>>>>> Stashed changes
            for flight_operator in flight_operators:
                sim.flight_operators.add(flight_operator)
                flight_operator.sim_list.add(sim)
                # Send notification
                send_mail(
                    'STaTE Simulation Added to Your Account',
                    'A new simulation, ' + sim.sim_name + ', has been added to your STaTE account.',
                    None,
                    [flight_operator.user.email],
                    fail_silently=False,
                )
            return redirect('tc:home')

    form = SimCreationForm()
    return render(request, 'tc/createSim.html', {'form': form})

###############################################################################

def addClass(request):

    if request.method == 'POST':
        form = ClassForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tc:home')
    else:
        form = ClassForm()
    return render(request, 'tc/addClass.html', {'form': form, 'title':'Add Class'})

###############################################################################
def tcSim(request, sim):
    simobj = Sim.objects.get(sim_name=sim)

    if request.method == 'POST':

        for subsystem in simobj.sys_list.all():
            if subsystem.sys_name in request.POST:
                form = SubsystemForm(request.POST, prefix=subsystem.sys_name, instance=subsystem)
                if form.is_valid():
                    #form.save_m2m()
                    form.save()
                    for flight_operator in simobj.flight_operators.all():
                        # Send notification
                        send_mail(
                            'STaTE: ' + sim,
                            'An anomoly has occured on your SimCraft: ' + sim + '.',
                            None,
                            [flight_operator.user.email],
                            fail_silently=False,
                        )
    print(simobj)
    forms = [SubsystemForm(prefix=subsystem.sys_name, instance=subsystem) for subsystem in simobj.sys_list.all()]
    return render(request, 'tc/tcSim.html', {'sim': simobj, 'forms': forms})
