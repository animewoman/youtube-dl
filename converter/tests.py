from django.test import TestCase
from .views import get_email
from .views import val_email
import youtube_dl
import os
from Youtub.settings import BASE_DIR


class GetEmailTest(TestCase):

    def test_email_sent(self):
        temp = get_email('pythondjangotestcase@gmail.com', 'asfdasf')
        self.assertEqual(temp, 1)

    def test_email_not_sent(self):
        temp = get_email('', 'asfdasf')
        self.assertEqual(temp, 0)


class EmailInvalidTest(TestCase):

    def test_email_invalid(self):
        temp = val_email('1111111111111111111111@gmail.com')
        self.assertEqual(temp, None)
        temp = val_email('pythondjangotestcase23141415@gmail.com')
        self.assertEqual(temp, None)

    def test_email_valid(self):
        temp = val_email('bekameilun@gmail.com')
        self.assertEqual(temp, True)
        temp = val_email('sididoma123@gmail.com')
        self.assertEqual(temp, True)


def get_audio(temp, x):
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

    if x == 0:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                temp, download=False,
            )
    else:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                temp
            )
    return meta['title']


class DownloadYoutubeTest(TestCase):

    def test_title(self):
        temp = get_audio('https://www.youtube.com/watch?v=PJVJUBvhbAY', 0)
        self.assertEqual(temp, 'asfdasf')

    def test_download(self):
        temp = get_audio('https://www.youtube.com/watch?v=PJVJUBvhbAY', 1)
        file_dir = os.path.join(BASE_DIR, 'audio/{}.mp3'.format(temp))
        self.assertRegexpMatches(file_dir, temp)
