from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from user.views import login_required_decorator
from main.models import Test, Questions, CheckQuestion, CheckTest, Category


# Create your views here.
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
