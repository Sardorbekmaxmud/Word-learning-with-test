from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language
from django.conf.urls import handler404

from user.views import SignUpView, logout_

handler404 = 'main.views.not_found_404.custom_404_view'

urlpatterns = [
    path('admin-secret/', admin.site.urls),

    path('set_language/', set_language, name='set_language'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('', include("main.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
