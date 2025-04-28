from django.contrib import admin

from .models import Category, Test, Questions

# Register your models here.
admin.site.register(Category)
admin.site.register(Test)
admin.site.register(Questions)
