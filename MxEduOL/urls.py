# coding: utf8
"""MxEduOL URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import xadmin

from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

# from users.views import user_login
from MxEduOL.settings import MEDIA_ROOT, STATIC_ROOT
from users.views import LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from users.views import IndexView
from organization.views import OrgView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),  # 智障地import了ModifyForm,然后.as_view() 。。。
    # 机构分支url
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程分支url
    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 配置静态文件处理函数
    url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
    # 用户分支url
    url(r'^users/', include('users.urls', namespace='users')),
]

handler403 = 'users.views.page_forbidden'
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
