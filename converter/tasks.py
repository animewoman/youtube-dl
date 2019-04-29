from celery import Celery
import youtube_dl
import os
from Youtub.settings import BASE_DIR
from .models import GetFiles
from django.core.mail import EmailMessage
from django.utils.timezone import now

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')


@app.task
def get_audio(temp):
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
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            temp
        )
    file_dir = os.path.join(BASE_DIR, 'media/audio/{}.mp3'.format(meta['title']))
    to_file = ''.join(file_dir.split())
    os.rename(file_dir, to_file)
    GetFiles.objects.create(name=meta['title'], pub_date=now())
    global x
    nums = len(meta['title']) + 4
    nums = len(file_dir) - nums
    x = to_file[nums:]
    return x


@app.task
def get_email(email):
    print('asdgasg')
    msg = EmailMessage('mp3-converter', 'http://127.0.0.1:8000/converter/download', to=[email])
    z = msg.send()
    return z
