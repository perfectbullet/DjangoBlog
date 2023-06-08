from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.urls import re_path
from django.views.static import serve

from DjangoBlog.admin_site import admin_site
from DjangoBlog.feeds import DjangoBlogFeed
from DjangoBlog.sitemap import StaticViewSitemap, ArticleSiteMap, CategorySiteMap, TagSiteMap, UserSiteMap

sitemaps = {
    'blog': ArticleSiteMap,
    'Category': CategorySiteMap,
    'Tag': TagSiteMap,
    'User': UserSiteMap,
    'static': StaticViewSitemap
}

handler404 = 'blog.views.page_not_found_view'
handler500 = 'blog.views.server_error_view'
handle403 = 'blog.views.permission_denied_view'
urlpatterns = [
                  url(r'^admin/', admin_site.urls),
                  url(r'', include('blog.urls', namespace='blog')),
                  url(r'mdeditor/', include('mdeditor.urls')),
                  url(r'', include('comments.urls', namespace='comment')),
                  url(r'', include('accounts.urls', namespace='account')),
                  url(r'', include('oauth.urls', namespace='oauth')),
                  url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                      name='django.contrib.sitemaps.views.sitemap'),
                  url(r'^feed/$', DjangoBlogFeed()),
                  url(r'^rss/$', DjangoBlogFeed()),
                  url(r'^search', include('haystack.urls'), name='search'),
                  url(r'', include('servermanager.urls', namespace='servermanager')),
                  url(r'', include('owntracks.urls', namespace='owntracks')),
                  re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
                  path("chat/", include("chat.urls")),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
