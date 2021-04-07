from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from subscriber.form import SubscriberCreateForm


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


# Wagtail Adminに項目が表示されてしまうので、context_processorにすべきかも？ -> To Do
@register_setting
class SubscriptionForm(BaseSetting):

  form = SubscriberCreateForm()