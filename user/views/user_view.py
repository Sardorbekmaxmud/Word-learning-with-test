from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from user.views import login_required_decorator
from user.forms import UpdateUserForm
from main.models import CheckTest, Test

User = get_user_model()


# Create your views here.
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

    return render(request=request, template_name='user/update_user.html', context={'form': form})
