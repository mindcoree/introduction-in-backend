# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Table
from .forms import TableForm

def table_list(request):
    tables = Table.objects.all()
    return render(request, 'tables/list.html', {'tables': tables})

def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_list')
    else:
        form = TableForm()
    return render(request, 'tables/create.html', {'form': form})

def available_tables(request):
    # Для примера: получаем дату через GET-параметры
    date = request.GET.get('date')
    time = request.GET.get('time')
    # Простейшая логика: отбираем столики, где is_available=True
    tables = Table.objects.filter(is_available=True)
    context = {'tables': tables, 'date': date, 'time': time}
    return render(request, 'tables/available.html', context)
