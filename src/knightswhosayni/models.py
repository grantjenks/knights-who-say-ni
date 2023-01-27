from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)


class Key(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
