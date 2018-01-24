from django import forms
from django.db import models
from wagtail.wagtailcore import blocks
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel,MultiFieldPanel, \
    InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

@register_snippet
class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'категории'
class NewsIndexPage(Page):
    intro = models.CharField(max_length=250)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super(NewsIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey('NewsPage', related_name='tagged_items')
class NewsPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Дата")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title",icon="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ],null=True,blank=True)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    categories = ParentalManyToManyField('news.NewsCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    search_fields = Page.search_fields + [
            index.SearchField('body'),
        ]
    content_panels = Page.content_panels + [
        FieldPanel('author'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Информация о блоге"),
        StreamFieldPanel('body'),
        InlinePanel('gallery_images', label="Фотография обложки"),
    ]

class NewsPageGalleryImage(Orderable):
        page = ParentalKey(NewsPage, on_delete=models.CASCADE, related_name='gallery_images')
        image = models.ForeignKey(
            'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
        )
        caption = models.CharField(blank=True, max_length=250)

        panels = [
            ImageChooserPanel('image'),
            FieldPanel('caption'),
        ]
class NewsTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = NewsPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(NewsTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
