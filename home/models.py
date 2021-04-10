from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks
from subscribers.form import SubscriberCreateForm


class HomePageCarouselImages(Orderable):
  """Between 1 and 5 images for the home page carousel."""

  page = ParentalKey("home.HomePage", related_name="carousel_images")
  carousel_image = models.ForeignKey(
    "wagtailimages.Image",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+"
  )
  image_alt = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    help_text='Add some alt text',
  )

  panels = [
    ImageChooserPanel("carousel_image"),
    FieldPanel("image_alt", heading="Image Alt (Option)"),
  ]


class HomePage(RoutablePageMixin, Page):
  """Home page model"""

  template = "home/home_page.html"
  max_count =1 # Only one homepage instance
  # parent_page_type = [
  #   'wagtailcore.Page'
  # ]

  banner_title = models.CharField(max_length=100, blank=False, null=True)
  banner_subtitle = RichTextField(features=["bold", "italic"])
  banner_image = models.ForeignKey(
    "wagtailimages.Image",
    null=True,
    blank=False,
    on_delete=models.SET_NULL,
    related_name="+"
  )
  banner_cta = models.ForeignKey(
    "wagtailcore.Page",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="+"
  )

  content = StreamField(
    [
      ("cta", blocks.CTABlock()),
    ],
    null=True,
    blank=True
  )

  content_panels = Page.content_panels + [
    MultiFieldPanel([
      FieldPanel("banner_title"),
      FieldPanel("banner_subtitle"),
      ImageChooserPanel("banner_image"),
      PageChooserPanel("banner_cta"),
    ], heading="Banner Options"),
    InlinePanel("carousel_images", max_num=5, min_num=1, label="Carousel Images"),
    StreamFieldPanel("content"),
  ]


  # # # def get_context_data(self, **kwargs):
  # # #   context = super().get_context_data(**kwargs) 
  # # def get_context(self, request):
  # #   context = super(HomePage, self).get_context(request)
  # def get_context(self, request, *args, **kwargs):
  #   context = super().get_context(request, *args, **kwargs)
  #   context['subscription_form'] = SubscriberCreateForm()
  #   return context

  class Meta:

    verbose_name = "Home Page"
    verbose_name_plural = "Home Pages"

  @route(r'^subscribe-route/$')
  def the_subscribe_page(self, request, *args, **kwargs):
    context = self.get_context(request, *args, **kwargs)
    context['subscription_form'] = SubscriberCreateForm()
    return render(request, "home/subscribe.html", context)

  # # 管理画面メニューのタイトルを変更
  # def get_admin_display_title(self):
  #   return "Main Pages"

