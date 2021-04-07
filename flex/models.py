from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from streams import blocks

class FlexPage(Page):
  """flexbile page class"""

  template = "flex/flex_page.html"

  subtitle = models.CharField(max_length=100, null=True, blank=True)

  content = StreamField(
    [
      ("title_and_text", blocks.TitleAndTextBlock()),
      ("full_richtext", blocks.RichTextBlock()),
      ("simple_richtext", blocks.SimpleRichTextBlock()),
      # ("simple_richtext", blocks.SimpleRichTextBlock(features=["bold", "italic"])),
      ("cards", blocks.CardBlock()),
      ("cta", blocks.CTABlock()),
      ("button", blocks.ButtonBlock()),
    ],
    null=True,
    blank=True
  )

  content_panels = Page.content_panels + [
    FieldPanel("subtitle"),
    StreamFieldPanel("content"),
  ]

  class Meta: # noqa

      verbose_name = "Flex Page"
      verbose_name_plural = "Flex Pages"
