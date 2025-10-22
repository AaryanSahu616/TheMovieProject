from django.db import models
from AccountsApp.models import User
import datetime

class Director(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Tags(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    title = models.CharField(max_length=100)
    synopsis = models.TextField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    release_date = models.DateField(default=datetime.date.today)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tags, related_name='tagged_movies', blank=True)

    def __str__(self):  
        return self.title
     
class UserReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/5)"
    


