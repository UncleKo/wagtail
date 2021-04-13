from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  modeladmin_register,
)
from .models import ContactPage

class ContactPageAdmin(ModelAdmin):

  model = ContactPage
  menu_label = "Contact Form"
  menu_icon = "folder"
  menu_order = 600
  add_to_settings_menu = False
  exclude_from_explorer = False
  list_display = ("title", "id")
  search_fields = ("title", "id")

modeladmin_register(ContactPageAdmin)
