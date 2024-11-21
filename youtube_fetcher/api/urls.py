from django.urls import path
from .views import FetchYouTubeDataView

urlpatterns = [
    path("fetch-youtube-data/", FetchYouTubeDataView.as_view(), name="fetch_youtube_data"),
]