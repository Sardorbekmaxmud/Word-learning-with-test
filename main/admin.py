from django.contrib import admin

from .models import Category, Test, Questions, CheckTest, CheckQuestion


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class QuestionsInline(admin.TabularInline):
    model = Questions


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline,]
    list_display = ('author__username', 'category__name', 'title', 'pass_percentage', 'created_at',)
    list_filter = ('author__username', 'category__name', 'title', 'pass_percentage',)
    search_fields = ('author__username', 'category__name', 'title',)
    ordering = ('created_at',)
    readonly_fields = ['created_at']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('test__title', 'title', 'a', 'b', 'c', 'd', 'true_option', 'created_at')
    list_filter = ('title',)
    search_fields = ('test__title', 'title',)
    ordering = ('created_at', 'true_option')
    readonly_fields = ['created_at']


admin.site.register([CheckTest, CheckQuestion])
