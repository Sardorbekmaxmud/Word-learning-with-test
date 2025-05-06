from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Test, Questions

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               error_messages={
                                   'required': 'Iltimos, foydalanadigan nomingizni kiriting!'
                               },
                               required=True,
                               label='Foydalanuvchi nomi:',
                               widget=forms.TextInput(attrs={'placeholder': 'Foydalanuvchi nomi',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=50,
                                help_text="Parolingiz kamida 8 ta belgidan iborat boʻlishi kerak. Sizning parolingiz tez-tez ishlatiladigan parol bo'lishi mumkin emas. Sizning parolingiz to'liq raqamli bo'lishi mumkin emas!",
                                required=True,
                                label="Parol:",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Parol',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password1',
                                                                  'id': 'password1',
                                                                  'name': 'password1',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                help_text='Verifikatsiya uchun parolingizni takroran yozing!',
                                required=True,
                                label="Parolni takrorlang:",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Parol',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password2',
                                                                  'id': 'password2',
                                                                  'name': 'password2',
                                                                  }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]
        labels = {
            'username': 'Foydalanuvchi nomi:',
            'password1': 'Parol:',
            'password2': 'Parolni takrorlang:',
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['category', 'title', 'pass_percentage']

    def save(self, request, commit=True):
        test = self.instance
        test.author = request.user
        super().save(commit)
        return test.id


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['title', 'a', 'b', 'c', 'd', 'true_option']

    submit_and_exit = forms.BooleanField(required=False)

    def save(self, test_id, commit=True):
        question = self.instance
        question.test = Test.objects.filter(pk=test_id).first()
        super().save(commit)
        return question
