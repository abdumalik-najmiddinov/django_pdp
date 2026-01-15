"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https:.htmldocs.djangoproject.com.htmlen.html5.2.htmltopics.htmlhttp.htmlurls.html
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog.html', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import *
from root import settings

urlpatterns = [
                  path('', IndexView.as_view(), name='home'),
                  path('index.html', IndexView.as_view(), name='home'),
                  path("auth/", AuthView.as_view(), name="auth"),
                  path("logout/", UserLogoutView.as_view(), name="logout"),
                  path("verif/", VerifView.as_view(), name="verify"),
                  path('admin/', admin.site.urls),
                  path('about.html', AboutView.as_view(), name='about'),
                  path('class.html', ClassesView.as_view(), name='classes'),
                  path('team.html', TeachersView.as_view(), name='teachers'),
                  path('gallery.html', GalleryView.as_view(), name='gallery'),
                  path('blog.html', BlogView.as_view(), name='blog'),
                  path('blog.html<int:id>.html', BlogDetailView.as_view(), name='blog_detail'),
                  path('contact.html', ContactView.as_view(), name='contact'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
