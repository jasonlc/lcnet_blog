from django.conf.urls import url
from blog.views import ArticleView,CategoryView,UserView,IndexView,CommentView,SearchView,AboutView,TagView,ArchiveView
from django.views.generic import TemplateView

urlpatterns=[
    url(r'^$',IndexView.as_view()),
    url(r'^article/(?P<slug>\w+).html',ArticleView.as_view()),
    url(r'^category/(?P<category>\w+)/$',CategoryView.as_view()),
    url(r'^user/(?P<slug>\w+)/$',UserView.as_view()),
    url(r'^login/$',TemplateView.as_view(template_name="blog/login.html")),
    url(r'^register/$',TemplateView.as_view(template_name="blog/register.html")),
    url(r'^comment/(?P<slug>\w+)$',CommentView.as_view()),
    url(r'^search/$',SearchView.as_view()),
    # url(r'^about/$',TemplateView.as_view(template_name="blog/about.html")),
    url(r'^about/$',AboutView.as_view()),
    url(r'^tag/(?P<tag>\w+)/$',TagView.as_view()),
    url(r'^archives/$',ArchiveView.as_view()),
]