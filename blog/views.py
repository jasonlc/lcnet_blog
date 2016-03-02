#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from blog.models import Article
from django.views.generic import View,ListView,DetailView
from django.core.cache import caches

try:
    cache=caches['memcache']
except ImportError as e:
    cache=caches['default']

class ArticleView(DetailView):
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
