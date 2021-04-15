from wagtail.contrib.modeladmin.options import (
  ModelAdmin,
  modeladmin_register,
)
from django.contrib.auth.models import User

class UserAdmin(ModelAdmin):

  model = User
  menu_label = "ユーザー"
  menu_icon = "user"
  menu_order = 520
  add_to_settings_menu = False
  exclude_from_explorer = False
  list_display = ("username", "is_staff", "first_name", "last_name", "email", "date_joined")
  search_fields = ("username", "is_staff", "first_name", "last_name", "email", "date_joined")
  # ordering = "-date_joined",
  # list_per_page = 100
  list_filter = ['is_staff']

modeladmin_register(UserAdmin)
