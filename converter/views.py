from __future__ import unicode_literals

import os
import time

import youtube_dl
from django.core.mail import EmailMessage
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from validate_email import validate_email

from Youtub.settings import BASE_DIR
from .forms import Download
from .models import GetFiles
import asyncio

x = ''


def val_email(email):
    return validate_email(email, verify=True)


async def get_audio(temp):
    ydl_opts = {
        'keepvideo': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'media/audio/%(title)s.mp3',
    }
    await asyncio.sleep(2)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            temp
        )
    file_dir = os.path.join(BASE_DIR, 'media/audio/{}.mp3'.format(meta['title']))
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


async def send_done():
    print('send_done')
    return HttpResponse('Link has been sent to your email')


async def get_email(email):
    await asyncio.sleep(2)
    print('asdgasg')
    msg = EmailMessage('mp3-converter', 'http://127.0.0.1:8000/converter/download', to=[email])
    z = msg.send()
    return z


def index(request):
    if request.POST:
        form = Download(request.POST)
        start = time.time()
        if form.is_valid():
            temp = form.cleaned_data.get('link')
            email = form.cleaned_data.get('email')
            if not val_email(email):
                return HttpResponse('Your email is invalid')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main(temp, email))
            loop.close()
            end = time.time()
            print(end - start, '\n\n\n')
    else:
        form = Download()

    return render(request, 'home.html', {'form': form})


def history(request):
    return render(request, 'history.html', {'options': GetFiles.objects.all()})


def download(request):
    global x
    print(x, '\n\n\n')
    file_dir = 'media/audio/{}'.format(x)
    print(file_dir, '\n\n\n')
    return render(request, 'download.html', {'link': file_dir})


async def main(temp, email):
    task1 = asyncio.ensure_future(get_audio(temp))
    task2 = asyncio.ensure_future(get_email(email))
    task3 = asyncio.ensure_future(send_done())
    await asyncio.gather(task1, task2, task3)
