#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from blog.models import Article,Category,Nav,Comment
from django.views.generic import View,ListView,DetailView,TemplateView
from django.db.models import Q
from django.core.cache import caches
from lcnet_blog.settings import PAGE_NUM
from django.core.exceptions import PermissionDenied
import logging
from django.db.models import Count

try:
    cache=caches['memcache']
except ImportError as e:
    cache=caches['default']
logger=logging.getLogger(__name__)
ArticleModel = Article
class BaseMixin(object):
    def get_context_data(self,*args,**kwargs):
        context=super(BaseMixin,self).get_context_data(**kwargs)
        try:
            context["categories"]=Category.objects.annotate(num_article=Count('article'))
            context["hot_article_list"]=Article.objects.order_by("-view_times")[0:10]
            context["nav_list"]=Nav.objects.filter(status=0)
            context["latest_comment_list"]=Comment.objects.order_by("-create_time")[0:10]
        except Exception as e:
            logger.error(u'加载基础信息出错')
        return context

class AboutView(TemplateView):
    template_name = "blog/about.html"
    def get_context_data(self,*args,**kwargs):
        context=super(AboutView,self).get_context_data(**kwargs)
        try:
            context["hot_article_list"]=Article.objects.order_by("-view_times")[0:10]
            context["nav_list"]=Nav.objects.filter(status=0)
            context["latest_comment_list"]=Comment.objects.order_by("-create_time")[0:10]
        except Exception as e:
            logger.error(u'加载基础信息出错')
        return context

class IndexView(BaseMixin,ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM #分页--每页的数目

    def get_context_data(self,**kwargs):
        #轮播
        # kwargs['carousel_page_list'] = Carousel.objects.all()
        return super(IndexView,self).get_context_data(**kwargs)

    def get_queryset(self):
        article_list = Article.objects.filter(status=0)
        return article_list

class TagView(BaseMixin,ListView):
    template_name = "blog/tag.html"
    context_object_name = "article_list"
    paginate_by = PAGE_NUM
    def get_queryset(self):
        tag=self.kwargs.get("tag","")
        article_list=Article.objects.only("tags").filter(tags__icontains=tag,status=0)
        return article_list

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

    def get_context_data(self, **kwargs):
        #评论
        en_title = self.kwargs.get('slug','')
        kwargs['comment_list'] = self.queryset.get(en_title=en_title).comment_set.all()
        return super(ArticleView,self).get_context_data(**kwargs)

class CategoryView(BaseMixin,ListView):
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

class CommentView(View):
    def post(self,request,*args,**kwargs):
        user=self.request.user
        comment=self.request.POST.get("comment","")
        if not user.is_authenticated():
            logger.error(u'[CommentView]当前用户为非活动用户:[%s]'%user.username)
            return HttpResponse(u'请先登陆！',status=403)
        if not comment:
            logger.error(u'[CommentView]当前用户输入空评论:[%s]' % user.username)
            return HttpResponse(u"请输入评论内容！",status=403)
        en_title=self.kwargs.get('slug','')
        try:
            article=ArticleModel.objects.get(en_title=en_title)
        except ArticleModel.DoesNotExist:
            logger.error(u'[CommentView]此文章不存在:[%s]' % en_title)
            raise PermissionDenied
        comment=Comment.objects.create(user=user,
                article=article,
                comment=comment,
                )
        try:
            img = comment.user.img
        except Exception as e:
            img = "http://vmaig.qiniudn.com/image/tx/tx-default.jpg"

        #返回当前评论
        html = "<li>\
                    <div class=\"lcnet-comment-tx\">\
                        <img src="+img+" width=\"40\"></img>\
                    </div>\
                    <div class=\"lcnet-comment-content\">\
                        <a><h1>"+comment.user.username+"</h1></a>"\
                        +u"<p>评论："+comment.comment+"</p>"+\
                        "<p>"+comment.create_time.strftime("%Y-%m-%d %H:%I:%S")+"</p>\
                    </div>\
                </li>"

        return HttpResponse(html)


class SearchView(BaseMixin,ListView):
    template_name = "blog/search.html"
    context_object_name = "article_list"
    paginate_by = PAGE_NUM

    def get_context_data(self,*args,**kwargs):
        kwargs['s']=self.request.GET.get('s','')
        return super(SearchView,self).get_context_data(**kwargs)
    def get_queryset(self):
        #获取搜索的关键字
        s = self.request.GET.get('s','')
        #在文章的标题,summary和tags中搜索关键字
        article_list = Article.objects.only('title','summary','tags')\
                .filter(Q(title__icontains=s)|Q(summary__icontains=s)|Q(tags__icontains=s)\
                ,status=0);
        return article_list
