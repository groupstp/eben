from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
    # TODO: добавить автоматическое добавление удаленного пользователя


# Create your models here.
class Task(models.Model):
    STATUS_CHOICE = [('new', _('new')), ('doing', _('doing')),
                     ('verifying', _('verifying')), ('returned', _('returned')),
                     ('done', _('done'))]

    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Task description'))
    author = models.ForeignKey('users.User',
                               on_delete=models.SET(get_sentinel_user),
                               verbose_name=_('Task author'),
                               related_name='task_author')
    doer = models.ForeignKey('users.User',
                             on_delete=models.SET(get_sentinel_user),
                             verbose_name=_('Doer'), related_name='task_doer')
    files = models.ManyToManyField('files.File',
                                   verbose_name=_("Attached files"),
                                   related_name='task_files')
    date_added = models.DateTimeField(_('Date added'))
    deadline = models.DateTimeField(_('Deadline'))
    status = models.CharField(_('Task status'), choices=STATUS_CHOICE,
                              default=STATUS_CHOICE[0][0], max_length=9)
    solution = models.TextField(_('Solution'))
    solution_files = models.ManyToManyField('files.File',
                                            verbose_name=_(
                                                'Attached solution files'),
                                            related_name='task_solution_files')
