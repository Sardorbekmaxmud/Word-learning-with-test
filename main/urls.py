from .signals import check_test, check_question
from django.urls import path
from .views import (index, detail, test, checktest,
                    create_category, create_test, create_question,
                    profile, update_user, update_test, delete_test)

urlpatterns = [
    # other urls
    path('', index, name='index'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    path('test/<int:test_id>/test/', test, name='test'),

    path('test/<int:checktest_id>/checktest/', checktest, name='checktest'),

    path('test/create_category/', create_category, name='create_category'),
    path('test/create_test/', create_test, name='create_test'),
    path('test/<int:test_id>/create_question/', create_question, name='create_question'),

    path('test/<int:test_id>/update/', update_test, name='update_test'),

    path('test/<int:test_id>/delete/', delete_test, name='delete_test'),

    # user
    path('profile/<int:user_id>/', profile, name='profile'),
    path('user/<int:user_id>/update', update_user, name='update_user'),
]
