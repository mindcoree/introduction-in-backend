from django.contrib import admin

# Register your models here.

from .models import Post, Thread

admin.site.register(Thread)
admin.site.register(Post)
