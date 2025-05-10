from .signals import check_test, check_question
from django.urls import path

from user.views import profile, update_user
from main.views import (index, all_categories, detail, test, checktest,
                        create_category, create_test, update_test,
                        update_category, delete_test, delete_category,)

urlpatterns = [
    # other urls
    path('', index, name='index'),
    path('category_list/', all_categories, name='category_list'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    path('test/<int:test_id>/test/', test, name='test'),

    # test --> check test
    path('test/<int:checktest_id>/checktest/', checktest, name='checktest'),

    # test --> create
    path('test/create_category/', create_category, name='create_category'),
    path('test/create_test/', create_test, name='create_test'),

    # test --> update
    path('test/<int:test_id>/update/', update_test, name='update_test'),
    path('test/category/<int:category_id>/update/', update_category, name='update_category'),

    # test --> delete
    path('test/<int:test_id>/delete/', delete_test, name='delete_test'),
    path('test/category/<int:category_id>/delete/', delete_category, name='delete_category'),

    # user
    path('profile/<int:user_id>/', profile, name='profile'),
    path('user/<int:user_id>/update', update_user, name='update_user'),
]
