from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Test, Questions, Category

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


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',  'first_name', 'last_name', 'email']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(),
        }

    yuborish_va_chiqish = forms.BooleanField(required=False, help_text="Boshqa kategoriya yaratmasangiz belgilang!")

    def __init__(self, *args, **kwargs):
        creating = kwargs.pop('creating', False)  # qo‘shimcha signal
        super().__init__(*args, **kwargs)

        if not creating:
            self.fields.pop('yuborish_va_chiqish')  # yangilashda yo‘qotish


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['category', 'title', 'pass_percentage']

    def save(self, request, commit=True):
        test = self.instance
        test.author = request.user
        super().save(commit)
        return test.id

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # foydalanuvchini olish
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)  # query ni o'zgartirish


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['title', 'a', 'b', 'c', 'd', 'true_option']

    yuborish_va_chiqish = forms.BooleanField(required=False, help_text="Boshqa savol yaratmasangiz belgilang!")

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
