from datetime import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from base_app.forms import VisitForm, CustomAuthenticationForm, CustomUserCreationForm
from base_app.models import Visit, Patient, Rehabilitator


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


@login_required
def index(request):
    context = {
        'message': 'Hello world!',
        'page': 'index'
    }
    return render(request, 'base_app/index.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'rehabilitator'))
def create_visit(request):
    form = VisitForm(initial={'rehabilitator': request.user.rehabilitator})
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visits')
        else:
            print(form.errors)
    context = {
        'form': form,
        'page': 'create_visit',
    }
    return render(request, 'base_app/create_visit.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'patient'))
def visits(request):
    context = {
        'visits': Visit.objects.filter(patient__isnull=True),
        'page': 'visits'
    }
    return render(request, 'base_app/visits.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'rehabilitator'))
def show_unconfirmed_visits(request):
    context = {
        'visits': Visit.objects.filter(patient__visit__isnull=False, accepted=False),
        'page': 'show_unconfirmed_visits',
    }
    return render(request, 'base_app/visits_to_confirm.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'patient'))
def assign_visit(request, pk):
    visit = Visit.objects.get(id=pk)
    visit.patient = request.user.patient
    visit.save()
    return redirect('visits')


@login_required
@user_passes_test(lambda u: hasattr(u, 'rehabilitator'))
def confirm_visit(request, pk):
    visit = Visit.objects.get(id=pk)
    visit.accepted = True
    visit.save()
    return redirect('visits_to_confirm')


@login_required
def show_visits_history(request):
    current_date = datetime.now().date()
    context = {
        'visits': Visit.objects.filter(start_date__lt=current_date),
        'page': 'show_visits_history'
    }
    return render(request, 'base_app/visits_history.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'patient'))
def add_feedback(request, pk):
    if request.method == 'POST':
        visit = Visit.objects.get(id=pk)
        visit.patient_feedback = request.POST['feedback']
        visit.save()
    return redirect('visits_history')


@login_required
def add_hospital_record(request, pk):
    if request.method == 'POST':
        patient = Patient.objects.get(id=pk)
        patient.description = request.POST['hospital_record']
        patient.save()
    return redirect('profile')


@login_required
def profile(request):
    context = {
        'page': 'profile'
    }
    return render(request, 'base_app/profile.html', context)


@login_required
def rehabilitators(request):
    context = {
        'rehabilitators': Rehabilitator.objects.all(),
        'page': 'rehabilitators',
    }
    return render(request, 'base_app/rehabilitator.html', context)
