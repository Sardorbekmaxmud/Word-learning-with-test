from django.urls import path
from .views import index, detail, profile

urlpatterns = [
    path('', index, name='index'),

    # test urls
    path('test/<int:test_id>/detail/', detail, name='detail'),
    # profile
    path('profile/', profile, name='profile'),
]
