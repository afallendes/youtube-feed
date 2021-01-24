from django.db import models
from django.contrib.auth.models import User

class YoutubeChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='UID', max_length=100)
    url = models.URLField(verbose_name='URL')
    title = models.CharField(max_length=250)
    #avatar = models.FilePathField(path='static/avatar')
    xml_url = models.URLField(verbose_name='XML URL')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class YoutubeVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(YoutubeChannel, on_delete=models.CASCADE)
    uid = models.CharField(verbose_name='UID', max_length=100)
    url = models.URLField(verbose_name='URL')
    title = models.CharField(max_length=250)
    description = models.TextField()
    #thumbnail = models.FilePathField(path='static/thumbnail')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
