from django.db import models
from django.utils import timezone
from eben.users.models import User


class Dialog(models.Model):
    name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    objects = models.Manager()


class User_to_dialog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    dialog = models.ForeignKey(Dialog, on_delete=models.PROTECT)
    time = models.DurationField()
    objects = models.Manager()
    num_new_mes = models.PositiveIntegerField(default=0)


class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    dialog = models.ForeignKey(Dialog, on_delete=models.PROTECT)
    status = models.BooleanField()
    status_del = models.BooleanField()
    time = models.DurationField()
    objects = models.Manager()

    class Meta:
        ordering = ["-time"]


class Message_to_user(models.Model):
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField()
    status_del = models.BooleanField()
    objects = models.Manager()


