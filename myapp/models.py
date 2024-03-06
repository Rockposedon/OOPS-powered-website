"""
from django.db import models
from django.contrib.auth.models import AbstractUser

# Abstract base class 'Media'
class Media(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)

    class Meta:
        abstract = True  # Making this class abstract, so it won't create a database table

    def play(self):
        # Abstract method, to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement the play method")

# Subclass 'Song' inheriting from 'Media'
class Song(Media):
    artist = models.CharField(max_length=100)

    def play(self):
        # Implementation of the play method for Song
        return f"Now playing: {self.title} by {self.artist}"

# 'User' model
class User(AbstractUser):
    # username = models.CharField(unique=True,max_length=50)
    email = models.EmailField(unique = True)
    
    def create_playlist(self, name):
        # Creating a playlist associated with the user
        playlist = Playlist(name=name, user=self)
        playlist.save()
        return playlist
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    def __str__(self) :
        return self.username

# 'Playlist' model
class Playlist(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)

    def play_all(self):
        # Playing all songs in the playlist and returning a list of results
        return [song.play() for song in self.songs.all()]
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Abstract base class 'Media'
class Media(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)

    class Meta:
        abstract = True  # Making this class abstract, so it won't create a database table

    def play(self):
        # Abstract method, to be implemented by subclasses
        raise NotImplementedError("Subclasses must implement the play method")

# Subclass 'Song' inheriting from 'Media'
class Song(Media):
    artist = models.CharField(max_length=100)

    def play(self):
        # Implementation of the play method for Song
        return f"Now playing: {self.title} by {self.artist}"

# 'User' model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def create_playlist(self, name):
        # Creating a playlist associated with the user
        playlist = Playlist.objects.create(name=name, user=self)
        return playlist
    # def __str__(self):
    #     return self.username
  

# 'Playlist' model
class Playlist(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)

    def play_all(self):
        # Playing all songs in the playlist and returning a list of results
        return [song.play() for song in self.songs.all()]
