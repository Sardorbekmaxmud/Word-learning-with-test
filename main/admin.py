from django.contrib import admin

from main.models import Category, Test, Questions, CheckTest, CheckQuestion


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('author__username', 'name',)
    list_filter = ('author__username', 'name',)
    search_fields = ('author__username', 'name',)
    ordering = ('name',)


class QuestionsInline(admin.TabularInline):
    model = Questions


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionsInline, ]
    list_display = ('author__username', 'category__name', 'title', 'pass_percentage', 'created_at',)
    list_filter = ('author__username', 'category__name', 'title', 'pass_percentage',)
    search_fields = ('author__username', 'category__name', 'title',)
    ordering = ('created_at',)
    readonly_fields = ['created_at']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('test__title', 'title', 'a', 'b', 'c', 'd', 'true_option', 'created_at')
    list_filter = ('test__title', 'title')
    search_fields = ('test__title', 'title',)
    ordering = ('created_at', 'true_option')
    readonly_fields = ['created_at']


class CheckQuestionInline(admin.TabularInline):
    model = CheckQuestion


@admin.register(CheckTest)
class CheckTestAdmin(admin.ModelAdmin):
    inlines = [CheckQuestionInline, ]
    list_display = ('solver__username', 'test__title', 'true_answers', 'percentage', 'is_passed', 'date')
    list_filter = ('solver__username', 'test__title', 'date', 'is_passed')
    search_fields = ('test__title', 'solver__username',)
    ordering = ('date',)
    readonly_fields = ['date']


@admin.register(CheckQuestion)
class CheckQuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'question__title', 'given_answer', 'true_answer', 'is_true', 'created_at',)
    list_filter = ('question__title',)
    search_fields = ('test__title', 'question__title',)
    ordering = ('created_at',)
    readonly_fields = ['created_at']
