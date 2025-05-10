from django.shortcuts import redirect, render

from main.models import Category, Questions
from main.forms import CategoryForm, TestForm, QuestionsCreateFormSet
from user.views import login_required_decorator


@login_required_decorator
def create_category(request):
    form = CategoryForm(creating=True)

    if request.method == "POST":
        form = CategoryForm(data=request.POST or None, creating=True)

        if form.is_valid():
            category = form.save(commit=False)
            category.author = request.user
            category.save()

            if form.cleaned_data['yuborish_va_chiqish']:
                return redirect('category_list')
            return redirect('create_category')

    context = {
        'form': form,
    }

    return render(request=request, template_name='test/create_category.html', context=context)


@login_required_decorator
def create_test(request):
    prefix = 'questions'
    number_of_category = Category.objects.filter(author=request.user).count()

    if request.method == "POST":
        form = TestForm(data=request.POST, user=request.user)
        formset = QuestionsCreateFormSet(request.POST, prefix=prefix)

        if form.is_valid():
            test_ = form.save(request=request, commit=False)
            test_.save()

            formset.instance = test_
            formset.save()

            # Savollarga qarab avtomatik o'tish foizini belgilash. 1 savol bo'lsa == 100%. 2 va undan ortiq savollar bo'lsa, 1 ta xato qilish mumkin.
            questions_of_test = Questions.objects.filter(test=test_).count()
            if questions_of_test and int(test_.pass_percentage) == 0:
                if questions_of_test > 1:
                    test_.pass_percentage = ((questions_of_test - 1) * 100) // questions_of_test
                else:
                    test_.pass_percentage = 100

            test_.save()

            return redirect('index')

    else:
        form = TestForm(user=request.user)
        formset = QuestionsCreateFormSet(prefix=prefix)

    context = {
        'form': form,
        'formset': formset,
        'formset_prefix': prefix,
        'number_of_category': number_of_category,
    }

    return render(request=request,
                  template_name='test/create_test.html',
                  context=context)
