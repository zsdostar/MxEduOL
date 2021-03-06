# coding:utf8
# __author__ = 'zsdostar'
# __date__ = '2017/6/9 14:55'
from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 用户个人信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像修改
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 修改邮箱的发送验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    # 完成修改邮箱的最后一步
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 用户课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),
    # 收藏机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 收藏教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 收藏课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage")
]
