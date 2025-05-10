from django.db import models
from django.contrib.auth import get_user_model

from main.models import Test, Questions

User = get_user_model()


# Create your models here.
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
