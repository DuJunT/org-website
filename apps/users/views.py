from django.shortcuts import render,reverse,redirect
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm,RegisterGetForm,RegisterPostForm,UploadImageForm,UserInfoForm,ChangePwdForm,ChangeMobileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
import redis
from apps.users.models import UserProfile
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.operations.models import UserMessage,Banner
from apps.courses.models import Course
from apps.organizations.models import CourseOrg
# print(settings.YP_APIKEY)

#APIKEY：de6b3f7745bfb241d943fcb9c13127b4


#首页
class IndexView(View):
    def get(self,request):
        #触发500错误
        # 1/0

        #触发403错误 限制访问
        # from django.core.exceptions import PermissionDenied
        # raise PermissionDenied

        #是否是广告位的课程
        is_banner_courses = Course.objects.filter(is_banner=True)[:3]
        not_banner_courses = Course.objects.filter(is_banner=False)

        #轮播图
        banners = Banner.objects.all().order_by('index')[:3]

        #课程机构
        course_orgs = CourseOrg.objects.all().order_by('learn_nums')[:15]
        # print(banners)
        content = {
            'banners':banners,
            'is_banner_courses':is_banner_courses,
            'not_banner_courses':not_banner_courses,
            'course_orgs':course_orgs,
        }
        return render(request,'index.html',context=content)

#登出
class LogoutView(View):

    def get(self,request):
        # 退出登录，将sessionid删除
        logout(request)
        return redirect(reverse('front:index'))

#登录
class LoginView(View):
    """
    djt 123456
    """
    def get(self,request):

        if request.user.is_authenticated:
            return redirect(reverse('front:index'))
        next = request.GET.get('next','')
        print(next)
        login_form = DynamicLoginForm()
        return render(request,'login.html',{'login_form':login_form,'next':next})


    def post(self,request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username= request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(username=username,password=password)  # 验证数据库中是否有该用户和密码
            if user is not None:
                #查询到用户
                # login方法会自动帮我们管理cookie和session
                login(request,user)
                next = request.GET.get('next','')
                if next:
                    return redirect(next)
                return redirect(reverse('front:index'))
            else:
                return render(request,'login.html',{'meg':'用户名或密码错误','forms':forms})
        else:
            # print(forms.errors.get_json_data())
            # print(forms.errors.items())
            return render(request,'login.html',{'forms_errors':forms.errors,'forms':forms})

# 发送验证码
class SendSmsView(View):
    def post(self,request):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}

        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data.get('mobile')
            code = generate_random(4,0)
            sms_json = send_single_sms(settings.YP_APIKEY,code,mobile)
            if sms_json['code'] == 0:
                r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)
                r.set(str(mobile),code)
                #设置过期时间
                r.expire(str(mobile),60*5)
                re_dict['status'] = 'success'
            else:
                re_dict['msg'] = sms_json['msg']

        else:
            print(send_sms_form.errors.get_json_data())
            for key,value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)

#动态登录
class DynamicLogin(View):
    def post(self,request):
        d_captcha_form = DynamicLoginForm()
        dynamic_active = False
        dynamic_login_form = DynamicLoginPostForm(request.POST)
        if dynamic_login_form.is_valid():
            mobile = dynamic_login_form.cleaned_data.get('mobile')
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10,2)
                user.set_password(password) #set_password函数给指定的参数加密
                user.mobile = mobile
                user.save()

            login(request,user)
            return redirect(reverse('front:index'))
        else:
            dynamic_active = True
            # print(dynamic_login_form.errors.get_json_data())
            # print(dynamic_login_form.errors)
            content = {
                'dynamic_login_form':dynamic_login_form,
                'dynamic_active':dynamic_active,
                'd_captcha_form':d_captcha_form,
                'dynamic_login_form_errors':dynamic_login_form.errors}
            return render(request,'login.html',context=content)

#注册
class RegisterView(View):
    def get(self,request):
        captcha_form = RegisterGetForm()
        return render(request,'register.html',{'captcha_form':captcha_form})

    def post(self,request):
        register_form = RegisterPostForm(request.POST)
        if register_form.is_valid():
            # 新建一个用户
            mobile = register_form.cleaned_data.get('mobile')
            password = register_form.cleaned_data.get('password')
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request,user)

            return redirect(reverse('front:index'))

        else:
            print(register_form.errors.get_json_data())
            captcha_form = RegisterGetForm()
            content = {
                'register_form_errors':register_form.errors,
                'captcha_form':captcha_form
            }
            return render(request,'register.html',context=content)

#上传文件
class UploadImageView(View):
    def post(self,request):

        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        # image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            # print(image_form)
            # image_form.save()
            image = image_form.cleaned_data.get('image')
            # print(request.user)
            user = UserProfile.objects.get(nick_name=request.user)
            user.image = image
            user.save()

            return JsonResponse({
                'status':'success'
            })
        else:

            return JsonResponse({
                'status': 'fail',
                'msg': '传入的图片格式不对'
            })

#个人中心
class UserCenterInfoView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        current_page = 'info'
        captcha_form = RegisterGetForm()
        content = {
            'captcha_form': captcha_form,
            'current_page': current_page,
        }
        # user = UserProfile.objects.filter(user)
        # print(request.user.birthday)
        return render(request,'usercenter-info.html',context=content)

    def post(self,request):
        userinfo_form = UserInfoForm(request.POST,instance=request.user)

        if userinfo_form.is_valid():
            userinfo_form.save()

            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(userinfo_form.errors)

#修改密码
class ChangePwdView(LoginRequiredMixin,View):
    login_url = '/login/'
    def post(self,request):
        pwd_form = ChangePwdForm(request.POST)

        if pwd_form.is_valid():
            pwd1 = pwd_form.cleaned_data.get('password1','')
            user = request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({
                'status':'success'
            })
        else:
            return JsonResponse(pwd_form.errors)

#修改手机号
class ChangeMobileView(LoginRequiredMixin,View):
    login_url = '/login/'
    # 需要验证手机号是否已经存在在数据库中（有没有被别人使用了）、验证输入的验证码是否正确（与redis中的code相比较）
    def post(self,request):
        mobile_form = ChangeMobileForm(request.POST)

        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data.get('mobile')
            mobile_existed = UserProfile.objects.filter(mobile=mobile)
            if mobile_existed:
                return JsonResponse({
                    'mobile':'该手机号已被使用'
                })
            user = request.user
            user.mobile = mobile
            user.save()
            return JsonResponse({
                'status':'success'
            })

        else:
            return JsonResponse(mobile_form.errors)

#我的课程
class MyCourseView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        print(request.path)
        current_page = 'mycourse'
        return render(request,'usercenter-mycourse.html',context={'current_page':current_page})

#我的消息
class MyMessageView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request):
        # 对课程机构进行分页
        messages = UserMessage.objects.filter(user=request.user)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=1, request=request)
        messages = p.page(page)

        content = {
            'messages': messages,

        }
        return render(request,'usercenter-message.html', context=content)