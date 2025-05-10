from django.shortcuts import render, redirect, get_object_or_404

from main.models import Category, Test, Questions
from main.forms import CategoryForm, TestForm, QuestionsFormSet
from user.views import login_required_decorator


@login_required_decorator
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    form = CategoryForm(instance=category, creating=False)

    if request.method == "POST":
        form = CategoryForm(data=request.POST or None, instance=category, creating=False)

        if form.is_valid():
            form.save()
            return redirect('category_list')

    return render(request=request, template_name='test/update_category.html', context={'form': form})


@login_required_decorator
def update_test(request, test_id):
    test_ = get_object_or_404(Test, pk=test_id)
    prefix = 'questions'

    if request.method == "POST":
        form = TestForm(data=request.POST, user=request.user, instance=test_)
        formset = QuestionsFormSet(request.POST, instance=test_, prefix=prefix)

        if form.is_valid() and formset.is_valid():
            form.save(request)
            formset.save()

            # Savollarga qarab avtomatik o'tish foizini belgilash .1 savol bo'lsa == 100%. 2 va undan ortiq savollar bo'lsa, 1 ta xato qilish mumkin.
            questions_of_test = Questions.objects.filter(test=test_).count()
            if questions_of_test and int(test_.pass_percentage) == 0:
                if questions_of_test > 1:
                    test_.pass_percentage = ((questions_of_test - 1) * 100) // questions_of_test
                else:
                    test_.pass_percentage = 100

            test_.save()

            return redirect('detail', test_id)
    else:
        form = TestForm(user=request.user, instance=test_)
        formset = QuestionsFormSet(instance=test_, prefix=prefix)

    return render(request=request, template_name='test/update_test.html', context={
        'form': form,
        'formset': formset,
        'formset_prefix': prefix,
    })
