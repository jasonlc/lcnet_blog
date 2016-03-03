#encoding:utf-8
from django.contrib import admin
from blog.models import Article,Category

class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title','summary')
    list_filter = ('status','category','create_time','update_time','is_top')
    list_display = ('title','category','status','is_top','update_time')
    fieldsets = (
        (u'基本信息', {
            'fields': ('title','category','en_title','img','tags','is_top','rank','status')
            }),
        (u'内容', {
            'fields': ('content',)
            }),
        (u'摘要', {
            'fields': ('summary',)
            }),
        (u'时间', {
            'fields': ('pub_time',)
            }),
    )

class CategoryAdmin(admin.ModelAdmin):
    search_fields =('name',)
    list_filter = ('status','create_time')
    list_display = ('name','parent','rank','status')
    fields = ('name','parent','rank','status')


admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)