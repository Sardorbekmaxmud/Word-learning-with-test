from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import CheckQuestion


@receiver(post_save, sender=CheckQuestion)
def check_test(sender, instance, *args, **kwargs):
    check_test = instance.test
    check_test.true_answers = CheckQuestion.objects.filter(test=check_test, is_true=True).count()

    try:
        check_test.percentage = check_test.true_answers * 100 // CheckQuestion.objects.filter(test=check_test).count()

        if check_test.test.pass_percentage <= check_test.percentage:
            check_test.is_passed = True
    except Exception as e:
        print("Xatolik: ", e)


@receiver(pre_save, sender=CheckQuestion)
def check_question(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True
    else:
        instance.is_true = False
