from django.db import models

from main.models import Test


# Create your models here.
class Questions(models.Model):
    STATUS_CHOICES = [
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=250, null=False, blank=False, help_text='Savol nomi')
    a = models.CharField(max_length=150, null=False, blank=False, help_text='Variant A')
    b = models.CharField(max_length=150, null=False, blank=False, help_text='Variant B')
    c = models.CharField(max_length=150, null=False, blank=False, help_text='Variant C')
    d = models.CharField(max_length=150, null=False, blank=False, help_text='Variant D')
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
