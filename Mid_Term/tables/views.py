from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Table
from .forms import TableForm

class TableListCreateView(View):
    def get(self, request):
        tables = Table.objects.all()
        return render(request, 'tables/table_list.html', {'tables': tables})

    def post(self, request):
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table-list-create')
        return render(request, 'tables/table_form.html', {'form': form})

class TableDetailView(View):
    def get(self, request, id):
        table = get_object_or_404(Table, id=id)
        return render(request, 'tables/table_detail.html', {'table': table})

class TableCreateView(View):
    def get(self, request):
        form = TableForm()
        return render(request, 'tables/table_form.html', {'form': form})

    def post(self, request):
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table-list-create')
        return render(request, 'tables/table_form.html', {'form': form})

class TableEditView(View):
    def get(self, request, id):
        table = get_object_or_404(Table, id=id)
        form = TableForm(instance=table)
        return render(request, 'tables/table_form.html', {'form': form})

    def post(self, request, id):
        table = get_object_or_404(Table, id=id)
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('table-list-create')
        return render(request, 'tables/table_form.html', {'form': form})

class TableDeleteView(View):
    def get(self, request, id):
        table = get_object_or_404(Table, id=id)
        return render(request, 'tables/table_confirm_delete.html', {'table': table})

    def post(self, request, id):
        table = get_object_or_404(Table, id=id)
        table.delete()
        return redirect('table-list-create')