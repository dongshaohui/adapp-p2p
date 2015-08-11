from django.conf.urls import patterns, include, url
from django.contrib import admin
from adapp.views import hello

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^hello/$', 'adapp.views.hello'),
	url(r'^$','p2p.views.p2pproduct',name='home'),
	
	url(r'^p2p/$', 'p2p.views.home'),
	url(r'^p2p/p2pproduct$','p2p.views.p2pproduct'),
	url(r'^uploadsm$','p2p.views.uploadsm'),
	
	url(r'^p2p/facematch$','p2p.views.facematch'),
	url(r'^p2p/info$','p2p.views.info'),
	url(r'^p2p/debug$','p2p.views.debug'),
	
	url(r'^upload_image$','p2p.views.upload_image'),
	
	# submit file
	url(r'^p2p/register$','p2p.views.register'),
	
)
