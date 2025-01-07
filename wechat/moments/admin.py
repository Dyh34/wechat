from django.contrib import admin
from .models import WeChatUser,Status

# Register your models here.

class StatusAdmin(admin.ModelAdmin):
    list_display = ["user","text","pics","pub_time"]
    search_fields = ["user__user__username","text","pics"]
    date_hierarchy = "pub_time"
    list_filter=["user__user__username","text"]

admin.site.register(WeChatUser)
admin.site.register(Status,StatusAdmin)
