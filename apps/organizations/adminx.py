import xadmin
from apps.organizations.models import Teacher, CourseOrg, City


class TeacherAdmin(object):
    list_display = ['name','age', 'work_year','org','add_time']
    search_fields = ['id', 'name','org__name']
    list_filter = ['name', 'work_year','org__name']


class CourseOrgAdmin(object):
    # pass
    list_display = ['id', 'name', 'desc', 'image', 'add_time' ]
    search_fields = ['id', 'name', 'desc']
    list_filter = ['name', 'desc']


class CityAdmix(object):
    """前面都是关键字，不可以修改的"""
    list_display = ['id', 'name', 'desc', 'add_time']  # 筛选需要显示的字段
    search_fields = ['id', 'name', 'desc']  # 搜索框
    list_filter = ['name', 'desc']  # 列表过滤器
    list_editable = ['name', 'desc']  # 定义可以修改的字段


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmix)
