from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import (
  FieldPanel,
  FieldRowPanel,
  InlinePanel,
  MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import (
  AbstractEmailForm,
  AbstractFormField
)

from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormField(AbstractFormField):
  page = ParentalKey(
    'ContactPage', 
    on_delete=models.CASCADE, 
    related_name='form_fields'
  )

# class ContactPage(AbstractEmailForm):
class ContactPage(WagtailCaptchaEmailForm):

  parent_page_types = ['home.HomePage']
  subpage_types = []

  template = "contact/contact_page.html"

  intro = RichTextField(blank=True)
  thank_you_text = RichTextField(blank=True)

  content_panels = AbstractEmailForm.content_panels + [
    FieldPanel('intro'),
    InlinePanel('form_fields', label='Form Fields'),
    FieldPanel('thank_you_text'),
    MultiFieldPanel([
      FieldRowPanel([
        FieldPanel('from_address', classname="col6"),
        FieldPanel('to_address', classname="col6")
      ]),
      FieldPanel("subject"),
    ], heading="Email Settings"),
  ]

register_snippet(ContactPage)
