from django.urls import path
from .views import *

urlpatterns = [
    # Movies API
    path("api/movies/", MovieListCreateAPIView.as_view(), name="movie_list_create"),
    path("api/movies/<int:pk>/", MovieRetrieveUpdateDestroyAPIView.as_view(), name="movie_detail"),

    # Add or update review API
    path("api/movies/<int:movie_id>/reviews/", AddOrUpdateReviewAPIView.as_view(), name="add_or_update_review"),
    path("", MovieTemplateListView.as_view(), name="movies_page"),

]
