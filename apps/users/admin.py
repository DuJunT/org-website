from django.contrib import admin
from apps.users.models import UserProfile
from django.contrib.auth.admin import UserAdmin
import xadmin


# class UserProfileAdmin(admin.ModelAdmin):
#     pass

# class UserProfileAdmin(object):
#     pass

# admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserProfile,UserAdmin)

# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile,UserProfileAdmin)