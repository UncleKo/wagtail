
from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  modeladmin_register,
)
from .models import BlogDetailPage

class BlogAdmin(ModelAdmin):
  """Subscriber admin."""

  model = BlogDetailPage
  menu_label = "Posts"
  menu_icon = "folder-open-1"
  menu_order = 290
  add_to_settings_menu = False
  exclude_from_explorer = False
  list_display = ("custom_title", "blog_image", "content")
  search_fields = ("custom_title", "blog_image", "content")

modeladmin_register(BlogAdmin)