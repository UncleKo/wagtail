
from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  modeladmin_register,
)
from .models import FlexPage

class FlexPageAdmin(ModelAdmin):
  """Subscriber admin."""

  model = FlexPage
  menu_label = "Flex Pages"
  menu_icon = "folder"
  menu_order = 300
  add_to_settings_menu = False
  exclude_from_explorer = False
  list_display = ("subtitle", "content")
  search_fields = ("subtitle", "content")

modeladmin_register(FlexPageAdmin)
