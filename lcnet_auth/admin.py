#encoding:utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from lcnet_auth.forms import LcNetUserCreationForm
from lcnet_auth.models import LcnetUser

class LcnetUserAdmin(UserAdmin):
    add_form = LcNetUserCreationForm
    add_fieldsets = (
        (None,{
            'classes':('wides',),
            'fields':('username','email','password','confirmpassword')
        })
    )
    fieldsets = (
        (u'基本信息', {'fields': ('username', 'password','email')}),
        (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (u'时间信息', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.unregister(Group)
admin.site.register(LcnetUser,LcnetUserAdmin)
