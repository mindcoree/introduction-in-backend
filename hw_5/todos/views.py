from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm
# Create your views here.

def login_view(request):
    login_dict = {'error':'Неверный логин или пароль'}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request,username,password)
        if user:
            login(request,user)
            return redirect('todo_list')
        else:
            return render(request,'login.html',login_dict)
    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def todo_list(request):
    todos = Todo.objects.filter(user = request.user)
    todos_dict = {'todos': todos}
    return render(request,'todos/todo_list.html',todos_dict)


@login_required
def todo_detail(request):
    todo = get_object_or_404(Todo,id,request.user)
    todo_dict = {'todo':todo}

    return render(request,'todos/todo_detail.html',todo_dict)


@login_required
def todo_add(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request,'todos/todo_add.html',{'form':form})


@login_required
def todo_delete(request,id):
    todo = get_object_or_404(Todo,id,request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request,'todos/todo_confirm_delete.html',{'todo':todo})

