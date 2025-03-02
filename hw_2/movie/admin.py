from django.contrib import admin
from .models import Movie  # Убедитесь, что импортируется из локального `models.py`

admin.site.register(Movie)
