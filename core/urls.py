"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from breakdowns import views as breakdown_views 
from django.contrib import admin

urlpatterns = [
    # Login to account URL mapper
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),

    # Logout URL mapper
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),

    # User Registration URL mapper
    url(r'^signup/$', breakdown_views.signup, name='signup'),

    # Breakdowns app urls
    url(r'^breakdowns/', include('breakdowns.urls')),

    # Redirect
    url(r'^$', RedirectView.as_view(url='/breakdowns/')),
    url(r'^admin/', admin.site.urls),
]
