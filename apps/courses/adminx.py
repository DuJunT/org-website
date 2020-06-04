import xadmin
from apps.courses.models import Course,Lesson,Video,CourseResource


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'teacher','course_org', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'teacher__name', 'add_time']
    list_filter = ['name', 'desc', 'degree', 'teacher__name', 'add_time']

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = [ 'name', 'add_time']
    list_filter = ['name', 'add_time']

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['name', 'add_time']
    list_filter = ['name', 'add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)