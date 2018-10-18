"""hotcow URL Configuration

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
from django.urls import path, include, re_path
from django.http import HttpResponse
from basicdata.views import BasisDataViewSet
from sk_optional import urls as sk_optional_url

def http404(request):
    return HttpResponse('<h1>404</h1>')

urlpatterns = [
    path('basisdata/', BasisDataViewSet.as_view(), name='获取基础数据'),
    path('skoptional/', include(sk_optional_url), name='自选'),
    re_path('.*', http404)
]
