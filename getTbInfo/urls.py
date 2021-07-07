"""getTbInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from user_auth import views as auth_view
from index import views as index_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', auth_view.reg, name='auth_reg'),
    path('login/', auth_view.login, name='auth_login'),
    path('logout/', auth_view.logout, name='auth_logout'),
    path('add_user/', auth_view.add_ajax, name='auth_add_user'),
    path('auth_user/', auth_view.auth_ajax, name='auth_auth_user'),
    path('homepage/', index_view.homepage, name='index_homepage'),
    path('search/', index_view.search, name='index_search'),
    path('result/<int:id>/', index_view.result_id, name='index_result_id'),
    path('result/', index_view.result, name='index_result'),
    path('history/', index_view.history, name='index_history'),
    path('history_data/', index_view.history_data, name='index_history_data'),
    path('ValidCodeImg/', auth_view.get_valid_code_img, name='get_valid_img'),
    # re_path(r'.*', index_view.jump_homepage, name='index_jump_homepage'),
]