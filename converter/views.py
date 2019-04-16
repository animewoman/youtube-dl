from __future__ import unicode_literals
from django.shortcuts import render
from .forms import Download
import youtube_dl
from .models import GetFiles
from django.shortcuts import HttpResponse
from django.utils.timezone import now
from django.core.mail import EmailMessage
from Youtub.settings import BASE_DIR
import os


def get_audio(temp):
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
    return meta['title']


def get_email(email, file):
    msg = EmailMessage('mp3-converter', 'message', to=[email])
    msg.content_subtype = 'html'
    file_dir = os.path.join(BASE_DIR, 'audio/{}'.format(file))
    msg.attach_file(file_dir)
    msg.send()


def index(request):
    if request.method == 'POST':
        form = Download(request.POST)
        if form.is_valid():
            link = form.cleaned_data
            temp = link['link']
            email = link['email']
            file_name = get_audio(temp)
            get_email(email, file_name)
            return HttpResponse('File has succesfully sent to your email')
    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def history(request):
    convert_to_list = GetFiles.objects.values_list('name', 'pub_date')
    convert_to_list = list(convert_to_list)
    return render(request, 'history.html', {'options': convert_to_list})
