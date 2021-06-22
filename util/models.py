from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Directory(models.Model):
    name = models.CharField(max_length = 30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.BooleanField(default = False)
    description = models.TextField(null = False)
    creation_date = models.DateTimeField(default = timezone.now)

    def __str__ (self):
        return self.name 

    def get_absolute_url(self):
        return ('/');

class File(models.Model):
    name = models.CharField(max_length = 30)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    directory = models.ForeignKey(Directory, on_delete = models.CASCADE)
    content = models.FileField(upload_to = 'database')
    deleted = models.BooleanField(default = False)
    framapath = models.CharField(max_length = 50, default="/")
    description = models.TextField()
    creation_date = models.DateTimeField(default = timezone.now)

    def __str__ (self):
        return self.name + " [" + str(self.pk) + "] "+ self.framapath + " " + self.content.url

    def get_absolute_url(self):
        return ('/');

class FileSection(models.Model):
    name = models.CharField(max_length = 30)
    description = models.TextField()
    creation_date = models.DateTimeField(default = timezone.now)
    category = models.CharField(max_length = 30)
    status = models.CharField(max_length = 30)
    status_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ('/');