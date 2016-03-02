from django.conf.urls import url
from blog.views import ArticleView

urlpatterns=[
    url(r'^article/(?P<slug>\w+).html',ArticleView.as_view()),
]