from django.db import models

class TodoList(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todos")

    def __str__(self):
        return self.title
