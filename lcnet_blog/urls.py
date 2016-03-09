from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    # Examples:
    # url(r'^$', 'lcnet_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'',include('blog.urls')),
    url(r'',include('lcnet_auth.urls')),
]
