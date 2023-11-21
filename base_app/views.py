from django.shortcuts import render, redirect
from base_app.forms import VisitForm
from base_app.models import Visit, Patient


def index(request):
    context = {
        'message': 'Hello world!'
    }
    return render(request, 'base_app/index.html', context)


def create_visit(request):
    form = VisitForm()
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'base_app/create_visit.html', context)


def visits(request):
    context = {
        'visits': Visit.objects.filter(patient__isnull=True)
    }
    return render(request, 'base_app/visits.html', context)


def assign_visit(request, pk):
    visit = Visit.objects.get(id=pk)
    visit.patient = Patient.objects.get(user=request.user)
    visit.save()
    return redirect('visits')
