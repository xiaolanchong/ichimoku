from django.conf.urls import patterns, include, url
from app.views import IndexView, AddCardView, DeckView, ExportDeckView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    url(r'^addcard$', AddCardView.as_view()),
    url(r'^mydeck$', DeckView.as_view()),
    url(r'^export$', ExportDeckView.as_view())
    # url(r'^ichimoku/', include('ichimoku.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
