# coding: utf-8
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
import os.path

class Area(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_("Name"), max_length=32)
    uuid = models.CharField(_("UUID"), max_length=48, unique=True)
    expiry = models.DateField(_("Expiration date"))
    max_size = models.IntegerField(_("Max size (MB)"), default=64)
    description = models.TextField()

    class Meta:
        unique_together = ["owner", "name"]

def get_upload_path(instance, filename):
    return os.path.join(instance.area.owner.username, instance.area.name, os.path.basename(filename))

class File(models.Model):
    area = models.ForeignKey(Area, related_name="files")
    file = models.FileField(upload_to=get_upload_path)
