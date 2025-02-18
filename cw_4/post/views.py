from django.shortcuts import render, redirect, get_object_or_404
from .models import Thread, Post
from .forms import ThreadForm, PostForm


def index(request):
    return redirect("thread_list")


def thread_list(request):
    threads = Thread.objects.all()
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thread_list")
    else:
        form = ThreadForm()

    return render(request, "threads/list.html", {"threads": threads, "form": form})


def thread_detail(request, id):
    thread = get_object_or_404(Thread, id=id)
    posts = thread.posts.all()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.save()
            return redirect("thread_detail", id=id)
    else:
        form = PostForm()

    return render(request, "threads/detail.html", {"thread": thread, "posts": posts, "form": form})


def thread_delete(request, id):
    thread = get_object_or_404(Thread, id=id)
    thread.delete()
    return redirect("thread_list")


def thread_edit(request, id):
    thread = get_object_or_404(Thread, id=id)
    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect("thread_detail", id=id)
    else:
        form = ThreadForm(instance=thread)

    return render(request, "threads/edit.html", {"form": form, "thread": thread})


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    thread_id = post.thread.id
    post.delete()
    return redirect("thread_detail", id=thread_id)


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    thread_id = post.thread.id

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("thread_detail", id=thread_id)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit.html", {"form": form, "post": post})
