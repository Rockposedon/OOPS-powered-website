# from django.shortcuts import render, redirect
# from .models import Song,User, Playlist
# from .lastfm_api import LastFMAPI
# from django.conf import settings
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import RegisterForm, LoginForm
# from django.contrib.auth import login as auth_login

# def landing_page(request):
#     return render(request, 'myapp/index.html')

# def list_songs(request):
#     query = request.GET.get("q", "")
#     api_key = settings.LASTFM_API_KEY
#     shared_secret = settings.LASTFM_SHARED_SECRET
#     lastfm_api = LastFMAPI(api_key=api_key, shared_secret=shared_secret)

#     search_results = lastfm_api.search_tracks(query)

#     # Ensure that each track has a valid preview_url before passing to the template
#     for track in search_results:
#         if not track.preview_url:
#             track.preview_url = 'https://example.com/default-preview-url.mp3'

#     return render(request, "myapp/search_results.html", {"tracks": search_results, "message": f"Search Results for '{query}'"})

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('list_songs')  # Redirect to your song list page
#     else:
#         form = RegisterForm()

#     return render(request, 'myapp/register.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)
#             return redirect('list_songs')  # Redirect to your song list page
#     else:
#         form = AuthenticationForm()

#     return render(request, 'myapp/login.html', {'form': form})

# def model_usage(request):
#     # Retrieve data from models
#     users = User.objects.all()
#     songs = Song.objects.all()
#     playlists = Playlist.objects.all()

#     context = {
#         'users': users,
#         'songs': songs,
#         'playlists': playlists,
#     }

#     return render(request, 'myapp/model_usage.html', context)

# def add_song_and_playlist(request):
#     # Assuming the user is authenticated
#     if request.user.is_authenticated:
#         # Create and save a new song
#         new_song = Song.objects.create(title="New Song", duration="3:30", artist="New Artist")

#         # Create and save a new playlist with the newly created song
#         new_playlist = Playlist.objects.create(name="New Playlist", user=request.user)
#         new_playlist.songs.add(new_song)

#         return render(request, 'myapp/success.html', {'message': 'Song and Playlist added successfully!'})
#     else:
#         # Handle the case when the user is not authenticated
#         return render(request, 'myapp/error.html', {'message': 'User not authenticated!'})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import the User model

from .models import Song, Playlist
from .lastfm_api import LastFMAPI
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login as auth_login

def landing_page(request):
    return render(request, 'myapp/index.html')

def list_songs(request):
    query = request.GET.get("q", "")
    api_key = settings.LASTFM_API_KEY
    shared_secret = settings.LASTFM_SHARED_SECRET
    lastfm_api = LastFMAPI(api_key=api_key, shared_secret=shared_secret)

    if query:
        # If a search query is provided, perform the search
        search_results = lastfm_api.search_tracks(query)

        # Ensure that each track has a valid preview_url before passing to the template
        for track in search_results:
            if not track.preview_url:
                track.preview_url = 'https://example.com/default-preview-url.mp3'

        return render(request, "myapp/search_results.html", {"tracks": search_results, "message": f"Search Results for '{query}'"})
    else:
        # If no search query, render a page with a message
        return render(request, "myapp/search_results.html", {"message": "Please enter a search query."})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('list_songs')  # Redirect to your song list page
    else:
        form = RegisterForm()

    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('list_songs')  # Redirect to your song list page
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})

def add_song_and_playlist(request, track_id):
    # Assuming the user is authenticated
    if request.user.is_authenticated:
        api_key = settings.LASTFM_API_KEY
        shared_secret = settings.LASTFM_SHARED_SECRET
        lastfm_api = LastFMAPI(api_key=api_key, shared_secret=shared_secret)

        # Retrieve track details from last.fm API
        track_details = lastfm_api.get_track_details(track_id)

        # Create and save a new song with last.fm details
        new_song = Song.objects.create(
            title=track_details.title,
            duration=track_details.duration,
            artist=track_details.artist,
            preview_url=track_details.preview_url
        )

        # Get or create a playlist associated with the user
        playlist, created = Playlist.objects.get_or_create(name="My Playlist", user=request.user)

        # Add the new song to the playlist
        playlist.songs.add(new_song)

        return redirect('list_songs')  # Redirect to your song list page
    else:
        # Handle the case when the user is not authenticated
        return render(request, 'myapp/error.html', {'message': 'User not authenticated!'})
    
def model_usage(request):
    # Retrieve data from models
    users = User.objects.all()
    songs = Song.objects.all()
    playlists = Playlist.objects.all()

    context = {
        'users': users,
        'songs': songs,
        'playlists': playlists,
    }

    return render(request, 'myapp/model_usage.html', context)