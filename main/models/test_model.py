from django.db import models
from django.contrib.auth import get_user_model

from main.models import Category

User = get_user_model()


# Create your models here.
class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Test turini tanlang")
    title = models.CharField(max_length=200, null=False, blank=False, help_text='Test nomi')
    pass_percentage = models.PositiveBigIntegerField(default=0, null=True, blank=True, help_text="O'tish foizi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        db_table = 'test'
        verbose_name_plural = 'tests'
