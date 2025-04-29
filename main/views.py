from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm
from .models import Test, Questions

User  =get_user_model()


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
    test = get_object_or_404(Test, pk=test_id)
    questions = Questions.objects.filter(test=test)
    return render(request=request, template_name='test/detail.html', context={'test': test, 'questions': questions})


@login_required_decorator
def profile(request):
    user = User.objects.filter(username=request.user).first()
    print(user.username, user.email)
    return render(request=request, template_name='profile/profile.html', context={'user': user})
