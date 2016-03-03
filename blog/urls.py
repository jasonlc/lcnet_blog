from django.conf.urls import url
from blog.views import ArticleView,CategoryView

urlpatterns=[
    url(r'^article/(?P<slug>\w+).html',ArticleView.as_view()),
    url(r'^category/(?P<category>\w+)/$',CategoryView.as_view()),
]