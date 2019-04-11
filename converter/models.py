from django.db import models


class GetFiles(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date')

