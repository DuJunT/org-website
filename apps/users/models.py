from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

GENDER_CHOICES = (
    ('male','男'),
    ('female','女'),
)

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20,null=True,verbose_name='昵称')
    birthday = models.DateField(verbose_name='生日',null=True)
    gender = models.CharField(verbose_name='性别',choices=GENDER_CHOICES,max_length=6)
    address = models.CharField(max_length=100,verbose_name='地址',null=True)
    # mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号码')
    mobile = models.CharField(max_length=11,verbose_name='手机号码')
    image = models.ImageField(upload_to='head_image/%Y/%m/%d',verbose_name='个人头像',default='default.jpg')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username

