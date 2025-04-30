from .signals import check_test, check_question
from django.urls import path
from .views import index, detail, test, profile

urlpatterns = [
    path('', index, name='index'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    path('test/<int:test_id>/test/', test, name='test'),
    # profile
    path('profile/', profile, name='profile'),
]
