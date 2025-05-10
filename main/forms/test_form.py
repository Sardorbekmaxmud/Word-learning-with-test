from django import forms

from main.models import Test, Category


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['category', 'title', 'pass_percentage']
        help_texts = {
            'pass_percentage': "Kiritmasangiz, avtomatik to'ldiriladi. 1-savol: 100%, 1 < bo'lsa, 1 xato qilish mumkin holatida.",
        }

    def save(self, request, commit=True):
        test = self.instance
        test.author = request.user
        super().save(commit)
        return test

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # foydalanuvchini olish
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)  # query ni o'zgartirish
