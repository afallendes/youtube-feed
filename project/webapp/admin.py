from django.contrib import admin

from webapp.models import Channel, Video

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('uid', 'title')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('uid', 'channel' , 'title')
