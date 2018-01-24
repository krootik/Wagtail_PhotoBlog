from __future__ import absolute_import, unicode_literals

from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from news.models import NewsPage
from news.models import NewsIndexPage
from albums.models import AlbumsPage
from albums.models import AlbumsIndexPage
from albums.models import AlbumsPageGalleryPage

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    def posts(self):
        posts = NewsPage.objects.all()
        posts = posts.order_by('-date')[:2]
        return posts
    def names(self):
        names = AlbumsPage.objects.all()
        names = names.order_by('-date')[:9]
        return names
    def titles(self):
        titles = NewsIndexPage.objects.all()
        titles = titles.order_by('id')
        return titles
    def titleGallery(self):
        titleGallery = AlbumsIndexPage.objects.all()
        titleGallery = titleGallery.order_by('id')
        return titleGallery
