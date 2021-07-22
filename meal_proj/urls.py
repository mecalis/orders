"""meal_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view
from profiles.views import UserFormView
from profiles.views import signup, activate, account_activation_sent
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path('', include('orders.urls', namespace='orders')),
    path('admin/', admin.site.urls),

    path('my-profile/', include('profiles.urls', namespace='profiles')),
    path('meals/', include('meals.urls', namespace='meals')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('register/', UserFormView.as_view(), name='register'),
    path('register/', signup, name='register'),

    path(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)