from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# class Profile(models.Model):
#   name = models.OneToOneField(to=User, on_delete=models.CASCADE)

class Subscription(models.Model):
  name = models.CharField(max_length=30)
  thumbnail = models.ImageField(upload_to='images/')
  last_updated = models.CharField(max_length=35)
  site_link = models.CharField(max_length=100)
  feed_link = models.CharField(max_length=100)

  def save(self):
    super().save()
    img = Image.open(self.thumbnail.path)  
    if img.height > 300 or img.width > 300:
      new_img = (500, 500)
      img.thumbnail(new_img)
      img.save(self.thumbnail.path)

  def __str__(self):
    return self.name

class Article(models.Model):
  subscription_name = models.ForeignKey(to=Subscription, on_delete=models.CASCADE)
  published = models.CharField(max_length=35)
  title = models.CharField(max_length=300)
  author = models.CharField(default=' ', max_length=100)
  summary = models.CharField(default=' ', max_length=500)
  media = models.ImageField(upload_to='images/')

  def __str__(self):
    return self.subscription_name.name + "'s Article"
