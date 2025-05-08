from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, TestForm, QuestionForm, CategoryForm, UpdateUserForm, QuestionsFormSet
from .models import Test, Questions, CheckQuestion, CheckTest, Category

User = get_user_model()


# Create your views here.
def login_required_decorator(func):
    return login_required(function=func, login_url='login')


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'


@login_required_decorator
def logout_(reqeust):
    logout(request=reqeust)

    return redirect('login')


@login_required_decorator
def index(request):
    queryset = Test.objects.filter(author=request.user)
    # queryset = Test.objects.filter(author=request.user).annotate(question_count=Count('questions'))

    context = {
        'tests': queryset,
    }
    return render(request=request, template_name='test/index.html', context=context)


@login_required_decorator
def all_categories(request):
    categories = Category.objects.filter(author=request.user)

    context = {
        'categories': categories,
    }
    return render(request=request, template_name='test/category_list.html', context=context)


@login_required_decorator
def detail(request, test_id):
    queryset = get_object_or_404(Test, pk=test_id)
    total_questions = Questions.objects.filter(test=queryset).count()
    return render(request=request, template_name='test/detail.html',
                  context={'test': queryset, 'total_questions': total_questions})


@login_required_decorator
def test(request, test_id):
    queryset = get_object_or_404(Test, pk=test_id)
    questions = Questions.objects.filter(test=queryset)

    if request.method == "POST":
        check_test = CheckTest.objects.create(solver=request.user, test=queryset)
        for question in questions:
            given_answer = request.POST[str(question.id)]

            CheckQuestion.objects.create(test=check_test,
                                         question=question,
                                         given_answer=given_answer,
                                         true_answer=question.true_option)
        check_test.save()

        return redirect('checktest', check_test.id)

    context = {
        'test': queryset,
        'questions': questions,
    }

    return render(request=request, template_name='test/test.html', context=context)


@login_required_decorator
def checktest(request, checktest_id):
    queryset = get_object_or_404(CheckTest, pk=checktest_id, solver=request.user)
    checkquestions = CheckQuestion.objects.filter(test=queryset)
    return render(
        request=request,
        template_name='test/checktest.html',
        context={
            'checktest': queryset,
            'checkquestions': checkquestions
        })


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
    form = TestForm(user=request.user)
    number_of_category = Category.objects.filter(author=request.user).count()

    if request.method == "POST":
        form = TestForm(data=request.POST, user=request.user)

        if form.is_valid():
            test_id = form.save(request=request)
            return redirect('create_question', test_id)

    context = {
        'form': form,
        'number_of_category': number_of_category,
    }

    return render(request=request,
                  template_name='test/create_test.html',
                  context=context)


@login_required_decorator
def create_question(request, test_id):
    queryset_test = get_object_or_404(Test, pk=test_id)

    if queryset_test.author == request.user:
        form = QuestionForm()

        if request.method == "POST":
            form = QuestionForm(data=request.POST)

            if form.is_valid():
                form_data_length = form.cleaned_data
                print(form_data_length)

                form.save(test_id)

                questions_of_test = Questions.objects.filter(test=test_id).count()
                if questions_of_test:
                    queryset_test.pass_percentage = ((questions_of_test - 1) * 100) // questions_of_test
                else:
                    queryset_test.pass_percentage = 0
                queryset_test.save()

                if form.cleaned_data['yuborish_va_chiqish']:
                    return redirect('index')
                return redirect('create_question', test_id)

        return render(request=request,
                      template_name='test/create_question.html',
                      context={'form': form, 'test': queryset_test})
    else:
        return HttpResponse("Sizga ruxsat yo'q! Negaki, siz testni egasi emassiz!")


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
            return redirect('detail', test_id)
    else:
        form = TestForm(user=request.user, instance=test_)
        formset = QuestionsFormSet(instance=test_, prefix=prefix)

    return render(request=request, template_name='test/update_test.html', context={
        'form': form,
        'formset': formset,
        'formset_prefix': prefix,
    })


@login_required_decorator
def delete_test(request, test_id):
    test_ = get_object_or_404(Test, pk=test_id)
    test_.delete()
    return redirect('index')


@login_required_decorator
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    return redirect('category_list')


@login_required_decorator
def profile(request, user_id):
    user = User.objects.filter(username=request.user).first()
    check_tests = CheckTest.objects.filter(solver=user_id)
    number_of_check_tests = check_tests.count()
    number_of_tests = Test.objects.filter(author=user_id).count()

    context = {
        'user': user,
        'number_of_checktests': number_of_check_tests,
        'number_of_tests': number_of_tests,
        'solved_tests': check_tests
    }

    return render(request=request, template_name='user/profile.html', context=context)


@login_required_decorator
def update_user(request, user_id):
    form = UpdateUserForm(instance=request.user)

    if request.method == "POST":
        form = UpdateUserForm(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile', user_id)

    context = {
        'form': form,
    }

    return render(request=request, template_name='user/update_user.html', context=context)
