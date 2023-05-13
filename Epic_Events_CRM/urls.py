"""
URL configuration for Epic_Events_CRM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from clients.views import ClientViewSet, ContractViewSet, ContractStatusViewSet, ReadEventViewSet, EventViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('clients', ClientViewSet, basename='clients')

router.register('contracts', ContractViewSet, basename='contracts')
router.register('signed_contracts', ContractStatusViewSet, basename='signed_contracts')

router.register("events", ReadEventViewSet, basename="events")
router.register(r"^(?P<contract_id>[^/.]+)/events", EventViewSet, basename="event")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('crm/', include(router.urls))
]
