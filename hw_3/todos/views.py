from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm

class TodoListView(ListView):
    model = Todo
    template_name = 'todos/list.html'
    context_object_name = 'todos'

class TodoDetailView(DetailView):
    model = Todo
    template_name = 'todos/detail.html'

def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo-list')
    else:
        form = TodoForm()
    return render(request, 'todos/create.html', {'form': form})

class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todos/delete.html'
    success_url = reverse_lazy('todo-list')