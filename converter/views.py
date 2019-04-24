from __future__ import unicode_literals
from django.shortcuts import render
from .forms import Download
from .models import GetFiles
from django.shortcuts import HttpResponse
from django.utils.timezone import now
from django.core.mail import EmailMessage
from validate_email import validate_email
from Youtub.settings import BASE_DIR
import youtube_dl
import time
import os

x = ''


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
        'outtmpl': './converter/templates/converter/audio/%(title)s.mp3',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            temp
        )
    file_dir = os.path.join(BASE_DIR, 'converter/templates/converter/audio/{}.mp3'.format(meta['title']))
    to_file = ''.join(file_dir.split())
    print(file_dir, '\n', to_file)
    os.rename(file_dir, to_file)
    GetFiles.objects.create(name=meta['title'], pub_date=now())
    global x
    nums = len(meta['title']) + 4
    nums = len(file_dir) - nums
    x = to_file[nums:]
    print(x, '\n\n\n')
    return meta['title']


def get_email(email):
    msg = EmailMessage('mp3-converter', 'http://127.0.0.1:8000/converter/download', to=[email])
    z = msg.send()
    return z


def index(request):
    if request.method == 'POST':
        form = Download(request.POST)
        start = time.time()
        if form.is_valid():
            temp = form.cleaned_data['link']
            email = form.cleaned_data['email']
            if not val_email(email):
                return HttpResponse('Your email is invalid')
            get_audio(temp)
            get_email(email)
            end = time.time()
            print(end - start, '\n\n\n')
            return HttpResponse('File has succesfully sent to your email')
    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def history(request):
    return render(request, 'history.html', {'options': GetFiles.objects.all()})


def download(request):
    global x
    print(x, '\n\n\n')
    file_dir = '/audio/{}'.format(x)
    print(file_dir, '\n\n\n')
    return render(request, 'download.html', {'link': file_dir})
