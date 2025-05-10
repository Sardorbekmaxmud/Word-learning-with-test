from django import forms

from main.models import Questions, Test


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['title', 'a', 'b', 'c', 'd', 'true_option']

    def save(self, test_id, commit=True):
        question = self.instance
        question.test = Test.objects.filter(pk=test_id).first()
        super().save(commit)
        return question


QuestionsFormSet = forms.inlineformset_factory(
    Test, Questions,
    fields="__all__",
    extra=1,  # 1 bo‘sh form ko‘rsatish uchun
    can_delete=True  # delete qilishni qo'shish uchun
)

QuestionsCreateFormSet = forms.inlineformset_factory(
    Test, Questions,
    fields="__all__",
    extra=1,  # 1 bo‘sh form ko‘rsatish uchun
    can_delete=False
)
