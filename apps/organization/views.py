# coding:utf8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse

from .models import CourseOrg
from .models import CityDict
from .models import Teacher
from operation.models import UserFavourite

from .forms import UserAskForm
from courses.models import Course


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CourseOrg.objects.all()  # 课程机构
        hot_orgs = all_orgs.order_by('-click_num')[:3]
        all_citys = CityDict.objects.all()  # 城市

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))  # i是不区分大小写

        # 城市筛选
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 机构类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-students')
            elif sort == "courses":
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()  # 课程总数

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
        })


class AddUserAskView(View):
    # 用户添加咨询
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        # 收藏判断
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]  # 这里控制取出的老师数量
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    # 机构课程
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 收藏判断
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    # 机构介绍
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 收藏判断
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    # 机构讲师
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 收藏判断
        has_fav = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    # 用户收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)  # 因为空字符转换为int，后面联合查询filter会抛出异常。故用0为默认值。
        # MDZZ fav_id后面多打了一个空格导致。。。fav_id取不到值
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavourite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
            # 这里用success才能实时更新
        else:
            user_fav = UserFavourite()
            if (int(fav_id) > 0) and (int(fav_type) > 0):
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    # 授课教师列表页
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(work_position__icontains=search_keywords))  # i是不区分大小写

        # 课程总数
        teacher_nums = all_teachers.count()

        # 按需排序功能
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by('-click_num')

        # 讲师排行榜
        teacher_rank = all_teachers.order_by('-click_num')[:3]

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'teacher_rank': teacher_rank,
            'teacher_nums': teacher_nums,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()

        has_teacher_faved = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                has_org_faved = True

        teacher_rank = Teacher.objects.all().order_by('-click_num')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'teacher_rank': teacher_rank,
            "has_teacher_faved": has_teacher_faved,
            "has_org_faved": has_org_faved,
        })
