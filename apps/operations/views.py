from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import UserCollectionForms,CommentForms
from .models import UserCollection,CourseComments
from apps.courses.models import Course
from apps.organizations.models import CourseOrg,Teacher
# Create your views here.

class AddFavView(View):
    def post(self,request):

        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                'status':'fail',
                'msg':'用户未登录',
            })
        else:
            user_collection_forms = UserCollectionForms(request.POST)
            # print(user_collection_forms)
            if user_collection_forms.is_valid():
                collection_id = user_collection_forms.cleaned_data.get('collection_id')
                collection_type = user_collection_forms.cleaned_data.get('collection_type')
                # print(collection_id,collection_type)

                #判断是否已收藏
                is_existed = UserCollection.objects.filter(user=request.user,collection_id=collection_id,collection_type=collection_type)

                if is_existed:
                    is_existed.delete()

                    if collection_type == 1:
                        course = Course.objects.get(pk = collection_id)
                        course.collection_nums -= 1
                        course.save()

                    if collection_type == 2:
                        course_org = CourseOrg.objects.get(pk = collection_id)
                        course_org.collection_nums -= 1
                        course_org.save()

                    elif collection_type == 3:
                        teacher = Teacher.objects.get(pk = collection_id)
                        teacher.collection_nums -= 1
                        teacher.save()

                    return JsonResponse({
                        'status': 'success',
                        'msg':'收藏'
                    })
                else:
                    collections_user = UserCollection()
                    collections_user.user = request.user
                    collections_user.collection_id = collection_id
                    collections_user.collection_type = collection_type
                    collections_user.save()
                    return JsonResponse({
                        'status':'success',
                        'msg': '已收藏'
                    })
            else:
                return JsonResponse({
                    'status': 'fail',
                    'msg': '参数错误',
                })


class CommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录',
            })

        course_comment_form = CommentForms(request.POST)
        if course_comment_form.is_valid():
            course = course_comment_form.cleaned_data.get('course')
            comments = course_comment_form.cleaned_data.get('comments')
            course_comments = CourseComments(course=course, user=request.user, comments=comments)
            course_comments.save()

            return JsonResponse({
                'status': 'success'
            })
        else:
            # print(course_comment_form.errors.get_json_data())
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误',
            })
