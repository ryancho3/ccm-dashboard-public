from django.urls import path
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views
from . import views


app_name = 'campaigns'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(views.IndexView.as_view()) , name = 'index'),
    path('accounts/profile', views.user_profile, name='profile'),
    path('accounts/register', views.user_register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout', views.user_logout, name='logout'),
    path('accounts/password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('<str:campaign_code>', views.campaign_detail, name='campaign_detail'),
    path('<str:campaign_code>/<str:school_code>', views.count_then_redirect, name='redirect'),
]