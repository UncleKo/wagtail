
from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  ModelAdminGroup,
  modeladmin_register,
)
from .models import ArticleBlogPage, VideoBlogPage, BlogCategory, BlogAuthor


class ArticlePostAdmin(ModelAdmin):

  model = ArticleBlogPage
  menu_label = "Articles"
  menu_icon = "folder"
  # menu_order = 1
  # add_to_settings_menu = False
  # exclude_from_explorer = False
  list_display = ("title", "custom_title", "get_categories", "get_tags", "first_published_at")
  search_fields = ("title", "custom_title", "content")

  def get_categories(self, obj):
    return ",\n".join([category.name for category in obj.categories.all()])

  def get_tags(self, obj):
    return ",\n".join([tag.name for tag in obj.tags.all()])


class VideoPostAdmin(ModelAdmin):

  model = VideoBlogPage
  menu_label = "Videos"
  menu_icon = "folder"
  list_display = ("title", "custom_title", "get_categories", "get_tags", "first_published_at")
  search_fields = ("title", "custom_title", "content")

  def get_categories(self, obj):
    return ",\n".join([category.name for category in obj.categories.all()])

  def get_tags(self, obj):
    return ",\n".join([tag.name for tag in obj.tags.all()])

class BlogCategoryAdmin(ModelAdmin):

  model = BlogCategory
  menu_label = "Categories"
  menu_icon = "list-ul"
  # menu_order = 2
  # add_to_settings_menu = False
  # exclude_from_explorer = False
  list_display = ("name", "slug")
  search_fields = ("name")

class BlogAuthorAdmin(ModelAdmin):

  model = BlogAuthor
  menu_label = "Blog Author"
  menu_icon = "placeholder"
  list_display = ("name", "website")
  search_fields = ("name")

class BlogAdminGroup(ModelAdminGroup):
    menu_label = "Blog"
    menu_icon = "folder-open-1"
    menu_order = 290
    items = (ArticlePostAdmin, VideoPostAdmin, BlogCategoryAdmin, BlogAuthorAdmin)

# modeladmin_register(PostAdmin)
# modeladmin_register(BlogCategoryAdmin)
modeladmin_register(BlogAdminGroup)