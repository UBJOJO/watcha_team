from django.db import models
from django.utils import timezone

# Create your models here.
class Movie(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='영화 제목')
    content = models.TextField(verbose_name='줄거리')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    running = models.CharField(max_length=10, verbose_name='러닝타임', blank=True, null=True)
    age = models.CharField(max_length=10, verbose_name='나이제한', blank=True, null=True)
    reservationRate = models.CharField(max_length=10, verbose_name='예매율', blank=True, null=True)
    genre_set = models.ManyToManyField('Genre', blank=True, null=True)
    cast_set = models.ManyToManyField('Cast', blank=True, null=True)
    director_set = models.ManyToManyField('Director', blank=True, null=True)
    country_set = models.ManyToManyField('Country', blank=True, null=True)
    rank = models.CharField(max_length=20, verbose_name='순위', blank=True, null=True)
    poster = models.CharField(max_length=200, verbose_name='포스터', blank=True, null=True)
    pubDate = models.TextField(verbose_name='제작년도', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    movie_name = models.CharField(max_length=200, verbose_name='영화 제목', blank=True, null=True)
    comment = models.CharField(max_length=200, verbose_name='이 작품에 대한 생각을 자유롭게 표현해주세요.', blank=True, null=True)

    def __str__(self):
        return self.comment

class Score(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    movie_name = models.CharField(max_length=200, verbose_name='영화 제목', blank=True, null=True)
    star = models.IntegerField(verbose_name='별점 매기기', blank=True, null=True)

    def __int__(self):
        return self.star

class Genre(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Cast(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
