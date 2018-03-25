from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'newsletter.views.CreateMyModelView', name='CreateMyModelView'),
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^signup$', 'newsletter.views.signup', name='signup'),
    url(r'^myData$', 'newsletter.views.myData', name='myData'),
    url(r'^track$', 'newsletter.views.track', name='track'),
    #url(r'^checkstatus$', 'newsletter.views.checkstatus', name='checkstatus'),
    url(r'^login$', 'newsletter.views.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, documents_root = settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, documents_root = settings.MEDIA_ROOT)
