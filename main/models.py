from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'


class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    pass_percentage = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        db_table = 'test'
        verbose_name_plural = 'tests'


class Questions(models.Model):
    STATUS_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    a = models.CharField(max_length=150, null=False, blank=False)
    b = models.CharField(max_length=150, null=False, blank=False)
    c = models.CharField(max_length=150, null=False, blank=False)
    d = models.CharField(max_length=150, null=False, blank=False)
    true_option = models.CharField(max_length=2, choices=STATUS_CHOICES, null=False, blank=False,
                                   help_text="To'g'ri variantni tanlang!")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    class Meta:
        db_table = 'question'
        verbose_name_plural = 'questions'
