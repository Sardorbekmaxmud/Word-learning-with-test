from .signals import check_test, check_question
from django.urls import path
from .views import (index, detail, test,
                    checktest, create_test, create_question,
                    profile)

urlpatterns = [
    # other urls
    path('', index, name='index'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    path('test/<int:test_id>/test/', test, name='test'),
    path('test/<int:checktest_id>/checktest/', checktest, name='checktest'),
    path('test/create_test/', create_test, name='create_test'),
    path('test/<int:test_id>/create_question/', create_question, name='create_question'),

    # user
    path('profile/<int:user_id>/', profile, name='profile'),
]
