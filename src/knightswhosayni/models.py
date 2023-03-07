from django.db import models


class Project(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Key(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    gumroad_link = models.CharField(max_length=200)

    def __str__(self):
        return self.prefix


class License(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    key = models.ForeignKey(Key, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    code = models.CharField(max_length=100)
    days = models.IntegerField(default=0)

    def __str__(self):
        return self.user
