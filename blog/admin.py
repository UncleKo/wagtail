
from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  ModelAdminGroup,
  modeladmin_register,
)
from .models import ArticleBlogPage, VideoBlogPage, BlogCategory

class ArticlePostAdmin(ModelAdmin):
  """Subscriber admin."""

  model = ArticleBlogPage
  menu_label = "Posts"
  menu_icon = "folder"
  # menu_order = 1
  # add_to_settings_menu = False
  # exclude_from_explorer = False
  list_display = ("title", "custom_title", "first_published_at")
  search_fields = ("title", "custom_title", "content")

class VideoPostAdmin(ModelAdmin):
  """Subscriber admin."""

  model = VideoBlogPage
  menu_label = "Videos"
  menu_icon = "folder"
  list_display = ("title", "custom_title", "first_published_at")
  search_fields = ("title", "custom_title", "content")

class BlogCategoryAdmin(ModelAdmin):
  """Subscriber admin."""

  model = BlogCategory
  menu_label = "Categories"
  menu_icon = "list-ul"
  # menu_order = 2
  # add_to_settings_menu = False
  # exclude_from_explorer = False
  list_display = ("name", "slug")
  search_fields = ("name")

class BlogAdminGroup(ModelAdminGroup):
    menu_label = "Blog"
    menu_icon = "folder-open-1"
    menu_order = 290
    items = (ArticlePostAdmin, VideoPostAdmin, BlogCategoryAdmin)

# modeladmin_register(PostAdmin)
# modeladmin_register(BlogCategoryAdmin)
modeladmin_register(BlogAdminGroup)