from __future__ import unicode_literals
from django.shortcuts import render
from .forms import Download
import youtube_dl
from django.views.static import serve
import os
from .models import GetFiles
from django.shortcuts import HttpResponse


def index(request):
    if request.method == 'POST':
        form = Download(request.POST)
        if form.is_valid():
            data = ''
            link = form.cleaned_data
            temp = link['link']
            for x in range(len(temp)):
                if temp[x] == '=':
                    for n in range(x + 1, len(temp)):
                        data += temp[n]
                    break
            x = GetFiles.objects.create(name=data)
            x.save()
            ydl_opts = {
                'keepvideo': True,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './audio/{}'.format(data),
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link['link']])
            print(GetFiles.objects.values_list('name'))
            return download(request, data)

    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def download(request, data):
    filepath = 'audio/{}'.format(data)
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))


def history(request):
    return HttpResponse(GetFiles.objects.values_list('name'))