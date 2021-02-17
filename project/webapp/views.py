from django.shortcuts import render, HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required

from .forms import AddChannelForm
from .logic import YouTubeChannelScraper
from .models import Channel, Video, User

@login_required
def list_videos(request):
    if request.method == 'GET':
        videos = Video.objects.filter(user=request.user)
        return render(request, 'webapp/list_videos.html', {'videos': videos})

def add_channel(request):
    if request.method == 'POST':
        form = AddChannelForm(request.POST)
        if form.is_valid():
            channel_url = request.POST.get('url')
            channel = YouTubeChannelScraper(channel_url)
            channel.get()
            channel.update()

            user = User.objects.get(username=request.user)

            if not Channel.objects.filter(uid=channel.uid).exists():      
                channel_db = Channel(
                    user=user,
                    uid=channel.uid,
                    url=channel.url,
                    title=channel.title,
                    xml_url=channel.feedURL
                )
                channel_db.save()
            else:
                channel_db = Channel.objects.get(uid=channel.uid)
            
            for video in channel.feedEntries:
                if not Channel.objects.filter(uid=video['uid']).exists():
                    video_db = Video(
                        user=user,
                        channel=channel_db,
                        uid=video['uid'],
                        url=video['url'],
                        title=video['title'],
                        description=video['description']
                    )
                    video_db.save()
            return HttpResponse('OK')
    else:
        form = AddChannelForm()
    return render(request, 'webapp/add_channel.html', {'form': form})
