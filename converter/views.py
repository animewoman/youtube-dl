from __future__ import unicode_literals
from django.shortcuts import render
from .forms import Download
from .models import GetFiles
from django.shortcuts import HttpResponse
from django.utils.timezone import now
from django.core.mail import EmailMessage
from Youtub.settings import BASE_DIR
from validate_email import validate_email
import youtube_dl
import os


def val_email(email):
    return validate_email(email, verify=True)


def get_audio(temp):
    ydl_opts = {
        'keepvideo': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': './audio/%(title)s.mp3',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            temp
        )

    GetFiles.objects.create(name=meta['title'], pub_date=now())
    return meta['title']


def get_email(email, file):
    msg = EmailMessage('mp3-converter', 'message', to=[email])
    file_dir = os.path.join(BASE_DIR, 'audio/{}.mp3'.format(file))
    msg.attach_file(file_dir)
    x = msg.send()
    return x


def index(request):
    if request.method == 'POST':
        form = Download(request.POST)
        if form.is_valid():
            temp = form.cleaned_data['link']
            email = form.cleaned_data['email']
            if not val_email(email):
                return HttpResponse('Your email is invalid')
            file_name = get_audio(temp)
            get_email(email, file_name)
            return HttpResponse('File has succesfully sent to your email')
    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def history(request):
    return render(request, 'history.html', {'options': GetFiles.objects.all()})
