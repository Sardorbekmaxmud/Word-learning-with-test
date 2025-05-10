from django.shortcuts import redirect, get_object_or_404

from main.models import Category, Test
from user.views import login_required_decorator


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
