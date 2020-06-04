from django import forms
from captcha.fields import CaptchaField
from django.conf import settings
import redis
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=2)
    password = forms.CharField(required=True,min_length=3)


class DynamicLoginForm(forms.Form):
    # myfield = AnyOtherField()
    captcha = CaptchaField()
    mobile = forms.CharField(required=True,min_length=11,max_length=11)


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True,max_length=11,min_length=11,error_messages={'required':'请输入手机号','max_length':'手机号位数为11位','min_length':'手机号位数为11位'})
    code = forms.CharField(required=True,min_length=4,max_length=4,error_messages={'required':'请输入您的手机验证码','min_length':'手机验证码位数为4','max_length':'手机验证码位数为4'})

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data.get('code')

        r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)
        r_code = r.get(str(mobile))
        if code != r_code:
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(min_length=11,max_length=11,required=True)
    code = forms.CharField(min_length=4,max_length=4,required=True)
    password = forms.CharField(required=True,min_length=6)

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile_exists = UserProfile.objects.filter(mobile=mobile)
        if mobile_exists:
            raise forms.ValidationError('该手机号已存在')
        return mobile

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data.get('code')

        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        r_code = r.get(str(mobile))
        if code != r_code:
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model =  UserProfile
        fields = ['nick_name','birthday','gender','address']


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5,max_length=20)
    password2 = forms.CharField(required=True,min_length=5,max_length=20)

    def clean(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 == pwd2:
            return self.cleaned_data
        else:
            raise forms.ValidationError('两次输入的密码不一致')


class ChangeMobileForm(forms.Form):
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
    code = forms.CharField(required=True,min_length=4,max_length=4)

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        code = self.cleaned_data.get('code')
        r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=0,charset='utf-8',decode_responses=True)
        redis_code = r.get(str(mobile))
        if redis_code != code:
            raise forms.ValidationError('验证码不正确')
