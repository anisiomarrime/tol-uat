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

from website.views import *

from website.views import download

app_name = 'website'


urlpatterns = [
    # Utilizando o {id} para buscar o objeto

    path('.well-known/acme-challenge/<str:slug>', download, name='download'),

    path('', IndexWebTemplateView.as_view(), name='index_web'),

    path('announcement/<slug:id>/', PostWebTemplateView.single, name='post_web'),

    path('announcements/', PostWebTemplateView.as_view(), name='posts_web'),

    path('how_to_buy/', HowToBuyTemplateView.as_view() , name='how_to_buy'),

    path('how_to_sell/', HowToSellTemplateView.as_view() , name='how_to_sell'),

    path('security_suggestions/', SecuritySuggestionsTemplateView.as_view() , name='security_suggestions'),


]
