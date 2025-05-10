from django import forms

from main.models import Category


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
