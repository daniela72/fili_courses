"""filicourses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    # above means: any urls that start with courses/ → send them to the urls module in the courses app
    # we write this line of code only once
    # below works well for index.html for the {% url 'courses:logout' %} for example
    # https://stackoverflow.com/questions/41883254/django-is-not-a-registered-namespace
    path('', include(('courses.urls', 'courses'), namespace='courses')),
]
