from django.shortcuts import render
from django.views import View
from .models import Course, CourseResource, Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.operations.models import UserCollection, UserCourse, CourseComments
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()

        #全局搜索
        keywords = request.GET.get('keywords','')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(tags__icontains=keywords)|Q(notice__icontains=keywords))

        # 热门课程推荐
        hot_courses = Course.objects.order_by('-clicks')[:3]

        # 对课程进行排序
        sort = request.GET.get('sort', '')
        if sort == '':
            all_courses = all_courses.order_by('-add_time')
        if sort == 'students':
            all_courses = all_courses.order_by('-learn_nums')

        if sort == 'hot':
            all_courses = all_courses.order_by('-collection_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=2, request=request)
        all_courses = p.page(page)

        content = {
            'all_courses': all_courses,
            'sort': sort,
            'hot_courses': hot_courses,

        }
        return render(request, 'course-list.html', context=content)


class CourseDetailView(View):
    def get(self, request, course_id):
        # 这里需要注意，不使用filter，因为filter返回的是一个QuerySet对象，这样传到前端中，需要遍历才能使用
        course = Course.objects.get(pk=course_id)
        # print(course)
        # print(type(course))
        course.clicks += 1
        course.save()

        has_coll_course = False
        has_coll_org = False

        if request.user.is_authenticated:
            if UserCollection.objects.filter(user=request.user, collection_id=course.id, collection_type=1):
                has_coll_course = True
            if UserCollection.objects.filter(user=request.user, collection_id=course.course_org.id, collection_type=2):
                has_coll_org = True

        # 通过课程的tags 来查询相关课程
        tag = course.tags
        relation_courses = []
        if tag:
            relation_courses = Course.objects.filter(tags=tag).exclude(pk=course.id)[:3]
            # print(type(relation_courses))
            # print(relation_courses)

        content = {
            'course': course,
            'has_coll_course': has_coll_course,
            'has_coll_org': has_coll_org,
            'relation_courses': relation_courses,
        }
        return render(request, 'course-detail.html', context=content)


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course_resources = CourseResource.objects.filter(course=course)

        # 判断是否有登录LoginRequiredMixin
        # 用户点“开始学习”就保存信息
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.learn_nums += 1
            course.save()

        # 查询学过该课程的 其他学生 ，从而查询该学生学习的其他课程
        other_user_courses = UserCourse.objects.exclude(user=request.user).exclude(course=course)
        print(other_user_courses)
        content = {
            'course': course,
            'course_resources': course_resources,
            'other_user_courses': other_user_courses,
        }
        return render(request, 'course-video.html', context=content)


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        course_resources = CourseResource.objects.filter(course=course)

        # 判断是否有登录LoginRequiredMixin
        # 用户点“开始学习”就保存信息
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.learn_nums += 1
            course.save()

        # 查询学过该课程的 其他学生 ，从而查询该学生学习的其他课程
        other_user_courses = UserCourse.objects.exclude(user=request.user).exclude(course=course)
        # print(other_user_courses)

        course_comments = CourseComments.objects.filter(course=course)

        content = {
            'course': course,
            'course_resources': course_resources,
            'other_user_courses': other_user_courses,
            'course_comments': course_comments,
        }
        return render(request, 'course-comment.html', context=content)


class CourseVideoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id):
        course = Course.objects.get(pk=course_id)
        course_resources = CourseResource.objects.filter(course=course)
        #视频
        video = Video.objects.get(pk=video_id)

        # 判断是否有登录LoginRequiredMixin
        # 用户点“开始学习”就保存信息
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.learn_nums += 1
            course.save()

        # 查询学过该课程的 其他学生 ，从而查询该学生学习的其他课程
        other_user_courses = UserCourse.objects.exclude(user=request.user).exclude(course=course)
        # print(other_user_courses)

        content = {
            'course': course,
            'course_resources': course_resources,
            'other_user_courses': other_user_courses,
            'video': video,
        }
        return render(request, 'course-play.html', context=content)
