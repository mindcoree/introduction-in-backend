from django.contrib import admin
from .models import Todo
# Register your models here.

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'user')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description')
    ordering = ('due_date',)
