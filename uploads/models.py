# coding: utf-8
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import os.path

class Area(models.Model):
    """
    A sharable file upload area
    """
    owner = models.ForeignKey(User)
    name = models.CharField(_("Name"), max_length=32)
    uuid = models.CharField(_("UUID"), max_length=48, unique=True)
    expiry = models.DateField(_("Expiration date"))
    max_size = models.IntegerField(_("Max size (MB)"), default=64)
    description = models.TextField()

    @property
    def expired(self):
        """
        True if the area is expired
        """
        return self.expiry < now().date()

    @property
    def size_percent(self):
        """
        Return the space currently in use as a percentage of the total size
        """
        return int(100.0 * self.size_used / (self.max_size * 1024 * 1024))

    @property
    def size_used(self):
        """
        Return the space currently in use for this area
        """
        return sum(f.file.size for f in self.files.all())

    class Meta:
        unique_together = ["owner", "name"]

def get_upload_path(instance, filename):
    return os.path.join(instance.area.owner.username, instance.area.name, os.path.basename(filename))

class File(models.Model):
    """
    An uploaded file
    """
    area = models.ForeignKey(Area, related_name="files")
    file = models.FileField(upload_to=get_upload_path)
