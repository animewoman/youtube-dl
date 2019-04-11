from __future__ import unicode_literals
from django.shortcuts import render
from .forms import Download
import youtube_dl
import datetime
from .models import GetFiles
from django.shortcuts import HttpResponse
from django.utils.timezone import now


def index(request):
    if request.method == 'POST':
        form = Download(request.POST)
        if form.is_valid():
            link = form.cleaned_data
            temp = link['link']
            ydl_opts = {
                'keepvideo': True,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './audio/%(title)s',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(
                    temp
                )

            x = GetFiles.objects.create(name=meta['title'], pub_date=now())
            x.save()
            return HttpResponse('File has succesfully downloaded in audio folder of this project')

    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def history(request):
    convert_to_list = GetFiles.objects.values_list('name', 'pub_date')
    convert_to_list = list(convert_to_list)
    return render(request, 'history.html', {'options': convert_to_list})
