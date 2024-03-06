from django.contrib import admin
from .models import Song, User, Playlist

admin.site.register(Song)
admin.site.register(User)
admin.site.register(Playlist)
