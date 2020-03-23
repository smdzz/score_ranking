from django.db import models


# Create your models here.
class ClientScore(models.Model):
    client = models.CharField(help_text='客户端', verbose_name='客户端', max_length=50, default='', null=False)
    score = models.IntegerField(null=False, blank=False, default=0)
