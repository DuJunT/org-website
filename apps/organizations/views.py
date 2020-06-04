from django.shortcuts import render
from django.views import View
from apps.organizations.models import CourseOrg,City
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from apps.organizations.forms import AskForm
from apps.operations.models import UserCollection
from django.db.models import Q
from apps.organizations.models import Teacher


class OrgView(View):
    def get(self,request):
        list_orgs = CourseOrg.objects.all()
        list_citys = City.objects.all()
        org_orders = list_orgs.order_by('-clicks')[:3]

        # 全局搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            list_orgs = list_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(tags__icontains=keywords))

        # 对机构类别进行筛选
        category = request.GET.get('ct','')
        if category:
            list_orgs = list_orgs.filter(category=category)

        # 对地区进行筛选
        city_id = request.GET.get('city','')
        if city_id:
            list_orgs = list_orgs.filter(city=city_id)

        # 对机构的学习人数和课程数量进行排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            list_orgs = list_orgs.order_by('-learn_nums')

        if sort == 'courses':

            list_orgs = list_orgs.order_by('-course_nums')



        # 对机构数量进行统计
        org_nums = list_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(list_orgs, per_page=2,request=request)

        orgs = p.page(page)

        content = {
            'list_orgs':orgs,
            # 'MEDIA_URL':settings.MEDIA_URL,
            'list_citys':list_citys,
            'category':category,
            'city_id':city_id,
            'org_nums':org_nums,
            'sort':sort,
            'org_orders':org_orders,

        }
        return render(request,'org-list.html',context=content)

# 立即咨询类
class AskView(View):
    def post(self,request):
        userask_form = AskForm(request.POST)
        if userask_form.is_valid():

            user_ask = userask_form.save(commit=True)
            return JsonResponse({
                'status': 'successs',
            })
        else:
            # print(userask_form.errors.get_json_data())
            return JsonResponse({
                'status':'fail',
                'msg':'提交错误'
            })

class OrgHomeView(View):
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(pk=org_id)

        if course_org:
            course_org.clicks += 1
            course_org.save()

            has_collection = False
            if request.user.is_authenticated:
                user_collection = UserCollection.objects.filter(user=request.user,collection_id=course_org.id,collection_type=2)
                if user_collection:
                    has_collection = True


            # 取课程
            all_courses = course_org.course_set.all()[:3]
            # print(all_courses)

            # 查询教师
            teacher = course_org.teacher_set.all()[:1][0]
            # print(teacher)
        content = {
            'all_courses':all_courses,
            'course_org':course_org,
            'teacher':teacher,
            'current_page':current_page,
            'has_collection':has_collection,
        }

        return render(request,'org-detail-homepage.html',context=content)


class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(pk=org_id)  # 通过org_id来获取对应的机构信息
        teachers = course_org.teacher_set.all()  # 通过对应的机构信息来反向查询机构里面的老师信息
        print(teachers)
        content = {
            'teachers':teachers,
            'course_org':course_org,
            'current_page':current_page,
        }
        return render(request,'org-detail-teachers.html',context=content)

class OrgDescView(View):
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(pk=org_id)
        content = {
            'course_org':course_org,
            'current_page':current_page,
        }
        return render(request,'org-detail-desc.html',context=content)

class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(pk=org_id)
        all_course = course_org.course_set.all()
        content = {
            'course_org':course_org,
            'all_course':all_course,
            'current_page':current_page,
        }
        return render(request,'org-detail-course.html',context=content)


class TeacherView(View):
    def get(self,request):
        teachers = Teacher.objects.all()
        # 人气（收藏数）排行
        sort = request.GET.get('sort','')
        if sort == 'hot':
            teachers = teachers.order_by('-collection_nums')

        #讲师排行
        rank_teachers = teachers.order_by('-work_year','clicks')[:3]

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1


        p = Paginator(teachers, per_page=2,request=request)

        #分页过后的老师
        p_teachers = p.page(page)

        context = {
            'teachers':teachers,
            'p_teachers':p_teachers,
            'sort':sort,
            'rank_teachers':rank_teachers,
        }
        return render(request,'teachers-list.html',context=context)

class TeacherDetailView(View):
    def get(self,request,t_id):
        teacher = Teacher.objects.filter(pk=t_id)[0]
        print(teacher)
        return render(request,'teacher-detail.html',locals())