from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'},
       name='logout'),
    #url(r'^main/$', views.getall, name='main'),
    url(r'^info/uptime/$', views.uptime, name='uptime'),
    url(r'^info/temp/$', views.temp, name='temp'),
    url(r'^info/humidity/$', views.humidity, name='humidity'),
    url(r'^info/memory/$', views.memusage, name='memusage'),
    url(r'^info/cpuusage/$', views.cpuusage, name='cpuusage'),
    url(r'^info/getdisk/$', views.getdisk, name='getdisk'),
    url(r'^info/getusers/$', views.getusers, name='getusers'),
    url(r'^info/getips/$', views.getips, name='getips'),
    url(r'^info/gettraffic/$', views.gettraffic, name='gettraffic'),
    url(r'^info/proc/$', views.getproc),
    url(r'^info/getdiskio/$', views.getdiskio, name='getdiskio'),
    url(r'^info/loadaverage/$', views.loadaverage, name='loadaverage'),
    url(r'^info/platform/([\w\-\.]+)/$', views.platform_info, name='platform'),
    url(r'^info/getcpus/([\w\-\.]+)/$', views.getcpus, name='getcpus'),
    url(r'^info/getnetstat/$', views.getnetstat, name='getnetstat'),
    url(r'^info/startcollector/$', views.startcollector, name='collector'),
]

