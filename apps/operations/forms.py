from django import forms
from .models import UserCollection,CourseComments

class UserCollectionForms(forms.ModelForm):
    class Meta:
        model = UserCollection
        fields = ['collection_id','collection_type']


class CommentForms(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['course','comments']
