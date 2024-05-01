"""
URL configuration for TrueGarageApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path

from admin_app.views import ClientOrdersView, VinOrdersView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/orders/client_number/<str:phone_number>/', ClientOrdersView.as_view(), name='client-orders'),
    path('api/v1/orders/vin/<str:vin>/', VinOrdersView.as_view(), name='vin-orders'),
]
