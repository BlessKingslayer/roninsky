from django.contrib import admin

from .models import Comment
from roninsky.custom_site import custom_site
from roninsky.base_admin import BaseOwnerAdmin

# Register your models here.


@admin.register(Comment, site=custom_site)
class CommentRegister(BaseOwnerAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
