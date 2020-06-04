from django import forms
from apps.operations.models import UserAsk
import re


class AskForm(forms.ModelForm):
    mobile = forms.CharField(max_length=11,min_length=11,required=True)
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']
        # exclude = ['add_time']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        regex_mobile = r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法',code='mobile_invalid')