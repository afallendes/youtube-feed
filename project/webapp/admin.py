from django.contrib import admin

from webapp.models import YoutubeChannel, YoutubeVideo

@admin.register(YoutubeChannel)
class YoutubeChannelAdmin(admin.ModelAdmin):
    list_display = ('uid', 'title')

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ('uid', 'channel' , 'title')
