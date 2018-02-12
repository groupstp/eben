from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    avatar = models.ImageField(_('Picture of User'), blank=True, upload_to='avatars/%Y/%m/%d/')
    date_of_birth = models.DateField(_('Birth date of User'), name='date_of_birth', blank=True, null=True,
                                     editable=True)
    info = models.TextField(_('Short info about User'), name='info', max_length=200, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
