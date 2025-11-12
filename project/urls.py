"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

import management_app
from management_app.views import CustomLoginView, welcome_page


urlpatterns = [
    # Automatically redirect to login
    path("", RedirectView.as_view(url='index', permanent=False)),

    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name='logout'),

    # Admin page, meant for the dev
    path("admin/", admin.site.urls),
    # Overwritten login view
    path("accounts/login/", CustomLoginView.as_view(), name='login'),
    # Default logout behaviour, it is redirected to the login view base on the project's settings
    path("accounts/", include('django.contrib.auth.urls')),


    path("index/", welcome_page, name="index"),

    path("management/", include("management_app.urls"))
]

# Add this line at the end of the file
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

