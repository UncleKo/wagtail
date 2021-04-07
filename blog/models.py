from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks


class BlogAuthor(models.Model):
  """Blog author for snippets."""

  name = models.CharField(max_length=100)
  website = models.URLField(blank=True, null=True)
  image = models.ForeignKey(
    "wagtailimages.Image",
    on_delete=models.SET_NULL,
    null=True,
    blank=False,
    related_name="+",
  )

  panels = [
    MultiFieldPanel(
      [
        FieldPanel("name"),
        ImageChooserPanel("image"),
      ],
      heading="Name and Image",
    ),
    MultiFieldPanel(
      [
        FieldPanel("website"),
      ],
      heading="Links",
    ),

  ]

  def __str__(self):
    """String repr of this class."""
    return self.name

  class Meta: # noqa
    verbose_name = "Blog Author"
    verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogListingPage(RoutablePageMixin, Page):
  """Listing page lists all the Blog Detail Pages."""

  max_count =1 
  template = "blog/blog_listing_page.html"

  custom_title = models.CharField(
    max_length=100,
    blank=False,
    null=False,
    help_text='Overwrites the default title',
  )

  content_panels = Page.content_panels + [
    FieldPanel("custom_title"),
  ]

  def get_context(self, request, *args, **kwargs):
    """Adding custom stuff to our context."""
    context = super().get_context(request, *args, **kwargs)
    context["posts"] = BlogDetailPage.objects.live().public().order_by('-first_published_at')
    context["special_link"] = self.reverse_subpage('latest_posts')
    return context

  @route(r'^latest/$', name="latest_posts")
  def latest_blog_posts(self, request, *args, **kwargs):
    context = self.get_context(request, *args, **kwargs)
    # context["latest_posts"] = BlogDetailPage.objects.all().order_by('-id')[:1]
    # context["latest_posts"] = BlogDetailPage.objects.live().public().order_by('-id')[:1]
    # context["latest_posts"] = BlogDetailPage.objects.live().public().reverse()[:1]
    context["latest_posts"] = context["posts"][:1]
    return render(request, "blog/latest_posts.html", context)

  def get_sitemap_urls(self, request):
    # return [] # if you don't want this page on sitemap
    sitemap = super().get_sitemap_urls(request)
    sitemap.append(
      {
        "location": self.full_url + self.reverse_subpage("latest_posts"),
        "lastmod": (self.last_published_at or self.latest_revision_created_at),
        "priority": 0.9,
      }
    )

    return sitemap


class BlogDetailPage(Page):
  """Blog detail page."""

  custom_title = models.CharField(
    max_length=100,
    blank=False,
    null=False,
    help_text='Overwrites the default title',
  )
  blog_image = models.ForeignKey(
    "wagtailimages.Image",
    blank=False,
    null=True,
    related_name="+",
    on_delete=models.SET_NULL,
  )
  image_alt = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    help_text='Add some alt text',
  )

  content = StreamField(
    [
      ("title_and_text", blocks.TitleAndTextBlock()),
      ("full_richtext", blocks.RichTextBlock()),
      ("simple_richtext", blocks.SimpleRichTextBlock()),
      # ("simple_richtext", blocks.SimpleRichTextBlock(features=["bold", "italic"])),
      ("cards", blocks.CardBlock()),
      ("cta", blocks.CTABlock()),
    ],
    null=True,
    blank=True
  )

  content_panels = Page.content_panels + [
    FieldPanel("custom_title"),
    ImageChooserPanel("blog_image"),
    FieldPanel("image_alt", heading="Image Alt (Option)"),
    StreamFieldPanel("content"),
  ]