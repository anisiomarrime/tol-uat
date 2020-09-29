"""mozpexels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from dashboard.views import *


app_name = 'dashboard'


urlpatterns = [
    # Utilizando o {id} para buscar o objeto
    path('', IndexTemplateView.as_view(), name='index'),

    path('post/add', PostAddTemplateView.as_view(), name='post_add'),

    path('post/edit/<int:id>/', PostAddTemplateView.edit, name='post_edit'),

    path('post/list', PostListTemplateView.as_view(), name='post_list'),

    path('post/api/approve/<int:id>/', PostListTemplateView.approve, name='approve'),

    path('post/api/remove/<int:id>/', PostListTemplateView.remove, name='remove'),

    path('login/', LoginTemplateView.as_view(), name='login'),

    path('logout/', LogoutTemplateView.as_view(), name='logout'),

    path('register/', RegisterTemplateView.as_view(), name='register'),

    path('forgot_password/', ForgotPasswordTemplateView.as_view(), name='forgot_password'),

    path('change_password/', ChangePasswordTemplateView.as_view(), name='change_password'),

    path('profile/', ProfileTemplateView.as_view(), name='profile'),

    path('sellers/', SellerListTemplateView.as_view(), name='sellers'),

    path('seller/api/staff/<int:id>/', SellerListTemplateView.staff, name='staff'),

    path('seller/api/doc/<int:id>/', SellerListTemplateView.doc, name='doc'),

    path('seller/api/profile/', SellerListTemplateView.profile, name='profile'),

    path('payments/', PaymentsTemplateView.as_view(), name='payments'),

    path('requests/', RequestsTemplateView.as_view(), name='requests'),

    path('requests/upgrade/', RequestsTemplateView.upgrade, name='upgrade'),

    path('plans/', PlansTemplateView.as_view(), name='plans')
]