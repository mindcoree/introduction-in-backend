from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


# API ViewSets
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title']

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')
        if self.request.query_params.get('my_posts') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        """Ensure only the author can delete the post via API."""
        if self.request.user != instance.author:
            self.permission_denied(self.request, message="You are not the author of this post.")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        post_id = self.kwargs.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        if self.request.query_params.get('my_comments') == 'true' and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


# Template-based views
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    search_query = request.GET.get('search', '')
    my_posts = request.GET.get('my_posts') == 'true'

    if my_posts and request.user.is_authenticated:
        posts = posts.filter(author=request.user)
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    paginator = Paginator(posts, 9)  # 9 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {
        'posts': page_obj,
        'search_query': search_query,
        'my_posts': my_posts,
        'page_obj': page_obj
    })


def search(request):
    search_query = request.GET.get('search', '')
    my_posts = request.GET.get('my_posts') == 'true'
    posts = Post.objects.all().order_by('-created_at')

    if my_posts and request.user.is_authenticated:
        posts = posts.filter(author=request.user)
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    paginator = Paginator(posts, 9)  # 9 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Для AJAX-запросов возвращаем JSON
        posts_data = [{
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%B %d, %Y'),
            'is_author': request.user.is_authenticated and request.user == post.author
        } for post in page_obj]
        return JsonResponse({
            'posts': posts_data,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages
        })

    # Для обычных запросов рендерим шаблон
    return render(request, 'post_list.html', {
        'posts': page_obj,
        'search_query': search_query,
        'my_posts': my_posts,
        'page_obj': page_obj
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Post.objects.create(title=title, content=content, author=request.user)
            return redirect('post_list')
    return render(request, 'post_form.html')


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post.title = title
            post.content = content
            post.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'post_form.html', {'form': post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_delete_confirm.html', {'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    my_comments = request.GET.get('my_comments') == 'true'

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, text=text, author=request.user)
            return redirect('post_detail', pk=pk)

    comments = post.comments.all()
    if my_comments and request.user.is_authenticated:
        comments = comments.filter(author=request.user)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'my_comments': my_comments
    })


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=post_id)
    return redirect('post_detail', pk=post_id)


def user_login(request):
    if request.method == 'POST':
        login_field = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=login_field, password=password)
        if not user:
            try:
                user_obj = User.objects.get(email=login_field)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'post_list'))
        return render(request, 'login.html', {'error': 'Invalid login or password'})
    return render(request, 'login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already taken'})
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already taken'})
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('post_list')
        return render(request, 'register.html', {'error': 'All fields are required'})
    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return redirect('post_list')