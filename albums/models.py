from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailsearch import index

class AlbumsIndexPage(Page):
    intro = models.CharField(max_length=250)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(AlbumsIndexPage, self).get_context(request)
        gallerypages = self.get_children().live().order_by('-first_published_at')
        context['gallerypages'] = gallerypages
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
class AlbumsPage(Page):
    date = models.DateField("data")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

class AlbumsPageGalleryPage(Orderable):
    page = ParentalKey(AlbumsPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
