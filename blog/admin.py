#encoding:utf-8
from django.contrib import admin
from blog.models import Article,Category,Nav,Comment
from forms import ArticleForm

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    search_fields = ('title',)
    list_filter = ('status','category','is_top','create_time','update_time','is_top')
    list_display = ('title','category','author','status','is_top','update_time')
    fieldsets = (
        (u'基本信息', {
            'fields': ('title','en_title','category','tags','author','is_top','rank','status')
            }),
        (u'内容', {
            'fields': ('content',)
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

class NavAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','url','status','create_time')
    list_filter = ('status','create_time')
    fields = ('name','url','status')

class CommentAdmin(admin.ModelAdmin):
    search_fields = ('user_username','article_title',)
    list_display = ('user','article','create_time')
    list_filter = ('create_time',)
    fields = ('user','article','comment')

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Nav,NavAdmin)
admin.site.register(Comment,CommentAdmin)