from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView

from games.views import IndexPage


urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
    url(r'^', include('games.urls', namespace='games')),
    url(r'^a441a4cc8871.html$',
        TemplateView.as_view(template_name='yandex.html')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^about/', include('pages.urls', namespace='pages')),
    url(r'^robots.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain')),
    url(r'^favicon.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),
                             permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
