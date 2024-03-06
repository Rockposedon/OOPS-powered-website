# myapp/urls.py
from django.urls import path, include
from .views import list_songs, register, user_login,landing_page, model_usage, add_song_and_playlist
from django.contrib import admin
from .import views
urlpatterns = [
    path('',landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('list_songs/', list_songs, name='list_songs'),
    path('admin/', admin.site.urls),  # Assuming you want to link to the Django admin
    path('search_lastfm_tracks/', list_songs, name='search_lastfm_tracks'),
    path('model_usage/',model_usage,name='model_usage'),
    # path('add_song_and_playlist/', add_song_and_playlist, name='add_song_and_playlist'),
    path('add_song_and_playlist/<int:track_id>/', views.add_song_and_playlist, name='add_song_and_playlist'),

]
