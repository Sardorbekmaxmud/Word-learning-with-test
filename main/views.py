from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm
from .models import Test, Questions, CheckQuestion, CheckTest

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
    queryset = Test.objects.all()
    return render(request=request, template_name='test/index.html', context={'tests': queryset})


@login_required_decorator
def detail(request, test_id):
    queryset = get_object_or_404(Test, pk=test_id)
    total_questions = len(Questions.objects.filter(test=queryset))
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
def profile(request):
    user = User.objects.filter(username=request.user).first()
    return render(request=request, template_name='profile/profile.html', context={'user': user})
