from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Category(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False, help_text="Nomi")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'


class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Test turini tanlang")
    title = models.CharField(max_length=200, null=False, blank=False, help_text='Test nomi')
    pass_percentage = models.PositiveBigIntegerField(null=True, blank=True, help_text="O'tish foizi")
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


class CheckTest(models.Model):
    solver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checktests")
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    true_answers = models.PositiveIntegerField(default=0)
    percentage = models.PositiveBigIntegerField(default=0)
    is_passed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.test.title)}"

    def __repr__(self):
        return f"{str(self.test.title)}"


class CheckQuestion(models.Model):
    test = models.ForeignKey(CheckTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=2)
    true_answer = models.CharField(max_length=2)
    is_true = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.is_true)

    def __repr__(self):
        return str(self.is_true)
