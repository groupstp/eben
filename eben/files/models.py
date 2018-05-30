from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class File(models.Model):
    """
    Общее хранилище файлов
    """
    file = models.FileField(_('File'), upload_to='files/%Y/%m/%d/')
    date_added = models.DateTimeField(_('Date upload'), auto_now_add=True)
