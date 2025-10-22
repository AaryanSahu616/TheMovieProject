from django.urls import path
from .views import *

urlpatterns = [
    # Template View
    path('', MovieTemplateListView.as_view(), name='movie_list_template'),

    # Standard DRF APIs (for management)
    path('api/movies/', MovieListCreateAPIView.as_view(), name='api_movie_list_create'),
    path('api/movies/<int:pk>/', MovieRetrieveUpdateDestroyAPIView.as_view(), name='api_movie_detail'),

    # Review API (as expected by your frontend JS)
    path('api/movies/<int:movie_id>/reviews/', AddOrUpdateReviewAPIView.as_view(), name='api_movie_review'),
    
    # Random Fetching APIs
    path('api/random/tags/', RandomTagsAPIView.as_view(), name='api_random_tags'),
    path('api/random/directors/', RandomDirectorsAPIView.as_view(), name='api_random_directors'),
    path('api/random/genres/', RandomGenresAPIView.as_view(), name='api_random_genres'),

    # In your app's urls.py
    path('api/movies/filter/', MovieFilterListAPIView.as_view(), name='api_movie_filter'),
]
