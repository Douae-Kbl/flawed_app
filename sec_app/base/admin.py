from django.contrib import admin
from .models import task
# Register your models here.
#you have to register you rmodels here for them to show up on the admin panel for django

admin.site.register(task)