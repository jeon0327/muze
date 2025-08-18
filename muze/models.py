from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Concert(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    poster = models.ImageField(upload_to='posters/')
    description_image = models.ImageField(upload_to='descriptions/')
    created_at = models.DateTimeField(auto_now_add=True)
    lineup = models.CharField(max_length=200, blank=True, null=True)
    rating = models.CharField(max_length=100, blank=True, null=True)
    runtime = models.CharField(max_length=100, blank=True, null=True)
    performance_times = models.TextField(blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rrn = models.CharField(max_length=13, unique=True)


class Review(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #추가
    nickname = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nickname} - {self.rating}점'
