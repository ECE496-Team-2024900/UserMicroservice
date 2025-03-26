"""
URL configuration for userserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from userserver import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('users/get_clinician_info', views.get_clinician_info),
    path('users/get_all_patients', views.get_all_patients),
    path('users/get_patients', views.get_patients),
    path('users/get_patient_info', views.get_patient_info),
    path('users/get_patient_info_by_email', views.get_patient_info_by_email),
    path('users/add_clinician', views.add_clinician),
    path('users/check_if_clinician_exists', views.check_if_clinician_exists),
    path('users/search_patients', views.search_patients),
    path('users/create_patient', views.create_patient),
    path('users/send_email', views.send_email),
    path('users/send_message', views.send_message),
    path('users/update_clinician_info', views.update_clinician_info)
]
