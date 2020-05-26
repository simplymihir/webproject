from django.contrib import admin
from .models import post

#to add any model to the admin page so that superuser can do whatever with it within admin.
# also you are required to import that model first
admin.site.register(post)

