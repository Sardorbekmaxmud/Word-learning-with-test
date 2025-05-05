from .signals import check_test, check_question
from django.urls import path
from .views import index, detail, test, checktest, profile

urlpatterns = [
    path('', index, name='index'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    path('test/<int:test_id>/test/', test, name='test'),
    path('test/<int:checktest_id>/checktest/', checktest, name='checktest'),
    # profile
    path('profile/', profile, name='profile'),
]
