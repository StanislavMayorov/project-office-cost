"""ProjectOfficeCost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from OfficeCost import views
from django.contrib.auth import views as django_auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', django_auth.login, name='login'),
    url(r'^logout/$', django_auth.logout, name='logout'),
    url(r'^limits/$', views.limits, name='limits'),
    url(r'^myexpenses/$', views.my_expenses, name='my_expenses'),
    url(r'^departmentexpenses/$', views.department_expenses, name='department_expenses'),
]
