from .models import UserAsk, UserCollection, CourseComments,\
    UserMessage, UserCourse,Banner
import xadmin


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCollectionAdmin(object):
    list_display = ['user', 'collection_id', 'collection_type', 'add_time']
    search_fields = ['user__nick_name', 'collection_id', 'collection_type', 'add_time']
    list_filter = ['user__nick_name', 'collection_id', 'collection_type', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['course', 'user', 'comments', 'add_time']
    search_fields = ['course__name', 'user__nick_name', 'comments', 'add_time']
    list_filter = ['course__name', 'user__nick_name', 'comments', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user__nick_name', 'message', 'has_read', 'add_time']
    list_filter = ['user__nick_name', 'message', 'has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__nick_name', 'course__name', 'add_time']
    list_filter = ['user__nick_name', 'course__name', 'add_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index']

xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCollection, UserCollectionAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
