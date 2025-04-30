from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import CheckTest, CheckQuestion


@receiver(post_save, sender=CheckTest)
def check_test(sender, instance, *args, **kwargs):
    instance.true_answers = CheckQuestion.objects.filter(test=instance, is_true=True).count()
    print(instance.true_answers, type(instance.true_answers))
    try:
        instance.percentage = instance.true_answers * 100 // CheckQuestion.objects.filter(test=instance).count()
        print(instance.percentage, type(instance.percentage))
        if instance.percentage >= instance.test.pass_percentage:
            instance.is_passed = True
    except Exception as e:
        print("Xatolik: ", e)


@receiver(pre_save, sender=CheckQuestion)
def check_question(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True
    else:
        instance.is_true = False
