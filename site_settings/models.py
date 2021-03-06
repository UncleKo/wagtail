from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from subscribers.form import SubscriberCreateForm


@register_setting
class SocialMediaSettings(BaseSetting):
  """Social media settings for our custom website."""

  facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
  twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
  youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel")

  panels = [
    MultiFieldPanel([
      FieldPanel("facebook"),
      FieldPanel("twitter"),
      FieldPanel("youtube"),
    ], heading="Social Medis Settings")
  ]


class SubscriptionForm(BaseSetting):

  form = SubscriberCreateForm()

