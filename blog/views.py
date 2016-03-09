#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from blog.models import Article,Category,Nav
from django.views.generic import View,ListView,DetailView,TemplateView
from django.core.cache import caches
from lcnet_blog.settings import PAGE_NUM
import logging

try:
    cache=caches['memcache']
except ImportError as e:
    cache=caches['default']
logger=logging.getLogger(__name__)

class BaseMixin(object):
    def get_context_data(self,*args,**kwargs):
        context=super(BaseMixin,self).get_context_data(*args)
        try:
            context["nav_list"]=Nav.objects.filter(status=0)
        except Exception as e:
            logger.error(u'加载基础信息出错')
        return context

class ArticleView(BaseMixin,DetailView):
    queryset=Article.objects.filter(status=0)
    template_name = 'blog/article.html'
    context_object_name = 'article'
    slug_field = 'en_title'
    def get(self, request, *args, **kwargs):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip=request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip=request.META['REMOTE_ADDR']
        self.cur_user_ip=ip
        en_title=self.kwargs.get('slug')
        visited_ips=cache.get(en_title,[])
        if ip not in visited_ips:
            try:
                article = self.queryset.get(en_title=en_title)
            except Article.DoesNotExist:
                raise Http404
            else:
                article.view_times+=1
                article.save()
                visited_ips.append(ip)
        cache.set(en_title,visited_ips,15*60)
        return super(ArticleView,self).get(request,*args,**kwargs)

    # def get_context_data(self, **kwargs):
    #     #评论
    #     en_title = self.kwargs.get('slug','')
    #     kwargs['comment_list'] = self.queryset.get(en_title=en_title).comment_set.all()
    #     return super(ArticleView,self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = "blog/category.html"
    context_object_name = "article_list"
    paginate_by = PAGE_NUM
    def get_queryset(self):
        category=self.kwargs.get('category','')
        try:
            article_list=Category.objects.get(name=category).article_set.all()
        except Category.DoesNotExist:
            raise Http404
        return article_list


class UserView(BaseMixin,TemplateView):
    template_name = "blog/user.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.error(u"[UserView]用户未登陆")
            return render(request,'blog/login.html')

        slug=self.kwargs.get("slug")

        if slug=="changetx":
            self.template_name="blog/user_changetx.html"
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug=="changepassword":
            self.template_name="blog/user_changepassword.html"
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'changeinfo':
            self.template_name = 'blog/user_changeinfo.html'
            return super(UserView,self).get(request,*args,**kwargs)

        logger.error(u'[UserView]不存在此接口')
        raise Http404
