from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from main.models import CheckQuestion


@receiver(post_save, sender=CheckQuestion)
def check_test(sender, instance, *args, **kwargs):
    check_test_ = instance.test
    check_test_.true_answers = CheckQuestion.objects.filter(test=check_test_, is_true=True).count()

    try:
        check_test_.percentage = check_test_.true_answers * 100 // CheckQuestion.objects.filter(test=check_test_).count()

        if check_test_.test.pass_percentage <= check_test_.percentage:
            check_test_.is_passed = True
        else:
            check_test_.is_passed = False
    except Exception as e:
        print("Xatolik: ", e)


@receiver(pre_save, sender=CheckQuestion)
def check_question(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True
    else:
        instance.is_true = False
