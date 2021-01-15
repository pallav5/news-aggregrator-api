from django.db import models
# Create your models here.

from django.contrib.auth.models import User


class Topic(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(null=True,blank=True)
  subscribed = models.BooleanField(default=False)
  subscriber = models.ManyToManyField(User, blank=True,null=True)

  def __str__(self):
    return self.title


class Headline(models.Model):
  topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()

  def __str__(self):
    return self.title


class Subscription(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  topic = models.ManyToManyField(Topic, blank=True)

  def __str__(self):
    return str(self.user)


