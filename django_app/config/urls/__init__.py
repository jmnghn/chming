from django.conf.urls import url, include

from config.urls import urls_views, urls_apis

urlpatterns = [
    url(r'', include(urls_views)),
    url(r'^api/', include(urls_apis)),
]