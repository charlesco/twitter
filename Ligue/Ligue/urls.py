from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^Ligue1/', include('Ligue1.urls')),
    url(r'^admin/', include(admin.site.urls)),
]