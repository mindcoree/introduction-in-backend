# posts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Post
from .forms import PostForm, LoginForm

def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("post_list")
        else:
            return render(request, "login.html", {"form": LoginForm(), "error": "Неверные данные"})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

def logout_view(request):
    logout(request)
    return redirect("login")

def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        form = PostForm() if request.user.is_authenticated else None
        return render(request, "posts/post_list.html", {"posts": posts, "form": form})
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Вы должны войти в систему для создания поста")
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_list")
        posts = Post.objects.all()
        return render(request, "posts/post_list.html", {"posts": posts, "form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "posts/post_list.html", {"posts": posts, "form": PostForm()})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Определяем, может ли пользователь редактировать/удалять пост
    can_edit = request.user == post.author
    can_delete = request.user == post.author or request.user.is_superuser
    return render(request, "posts/post_detail.html", {
        "post": post,
        "can_edit": can_edit,
        "can_delete": can_delete
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("У вас нет прав для редактирования этого поста")
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, "posts/post_form.html", {"form": form, "post": post})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", pk=pk)
        return render(request, "posts/post_form.html", {"form": form, "post": post})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

@login_required
@require_http_methods(["DELETE"])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("У вас нет прав для удаления этого поста")
    post.delete()
    # После удаления перенаправляем на страницу todos (здесь создан шаблон-заглушка)
    return JsonResponse({"redirect": "/todos/"})

def todos(request):
    return render(request, "todos.html")
