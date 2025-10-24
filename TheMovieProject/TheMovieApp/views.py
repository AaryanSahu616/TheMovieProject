# In your app's views.py (e.g., TheMovieApp/views.py)
from rest_framework import generics, status
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie, UserReview, Director, Genre, Tags
from .serializers import MovieSerializer, UserReviewSerializer, DirectorSerializer, GenreSerializer, TagSerializer # Assuming you create these
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView # Import for simple, non-model-bound APIs
from django.db.models import Count # Not strictly needed but useful for future analysis

# --- Template View ---

class MovieTemplateListView(LoginRequiredMixin, ListView):
    """
    Displays the list of all movies along with the current user's reviews.
    This view renders the HTML template.
    """
    model = Movie
    template_name = "TheMovieApp/movies.html" # Note: Using 'movies.html' as per your provided code
    context_object_name = "movies"

    def get_queryset(self):
        # Prefetch related models to optimize template rendering lookups
        return Movie.objects.all().select_related('director').prefetch_related('genre', 'tags').order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Fetch user reviews
        if self.request.user.is_authenticated:
            user_reviews = UserReview.objects.filter(user=self.request.user).select_related('movie')
            # Build a dict {movie_id: review} for fast lookup in template (as in your original code)
            context['user_reviews_dict'] = {r.movie_id: r for r in user_reviews}
        else:
            context['user_reviews_dict'] = {}
            
        return context

# ----------------------------------------------------------------------
# --- Standard DRF API Views (Keep these as they are) ---

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated] # Assuming all movie operations require auth

class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]


# --- DRF API Views for Random Data Fetching ---
# Using generics.ListAPIView for a clean, serializable response

class RandomTagsAPIView(generics.ListAPIView):
    """API to fetch a random sample of Tags."""
    # Fetch up to 10 random tags
    queryset = Tags.objects.all().order_by('?')[:10] 
    serializer_class = TagSerializer # Assuming TagSerializer exists
    # No permission class needed, usually random data is public

class RandomDirectorsAPIView(generics.ListAPIView):
    """API to fetch a random sample of Directors."""
    # Fetch up to 5 random directors
    queryset = Director.objects.all().order_by('?')[:5] 
    serializer_class = DirectorSerializer # Assuming DirectorSerializer exists

class RandomGenresAPIView(generics.ListAPIView):
    """API to fetch a random sample of Genres."""
    # Fetch up to 8 random genres
    queryset = Genre.objects.all().order_by('?')[:8]
    serializer_class = GenreSerializer # Assuming GenreSerializer exists

# ----------------------------------------------------------------------
# --- Review API (Keep this as it is, using GenericAPIView as in your original) ---

class AddOrUpdateReviewAPIView(generics.GenericAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        """
        Create or update a review for a given movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        # Convert rating to int immediately for reliable comparison
        rating = request.data.get("rating")
        review_text = request.data.get("review_text")

        # Basic Validation
        try:
            rating = float(rating)
            if not 0 <= rating <= 5:
                 return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
             return Response({"error": "Rating is required and must be an decimal."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure review_text is present, even if empty string
        if review_text is None:
            return Response({"error": "Review text is required (can be empty string)."},
                             status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has a review for this movie
        existing_review = UserReview.objects.filter(movie=movie, user=request.user).first()

        if existing_review:
            existing_review.rating = rating
            existing_review.review_text = review_text
            existing_review.save()
            return Response({"message": f"Review for '{movie.title}' updated successfully."})
        else:
            UserReview.objects.create(
                movie=movie,
                user=request.user,
                rating=rating,
                review_text=review_text,
            )
            return Response({"message": f"Review for '{movie.title}' added successfully."})
        
class MovieFilterListAPIView(generics.ListAPIView):
    serializer_class = MovieSerializer
    
    def get_queryset(self):
        queryset = Movie.objects.all().select_related('director').prefetch_related('genre', 'tags')
        
        # Get query parameters
        director_id = self.request.query_params.get('director_id')
        tag_id = self.request.query_params.get('tag_id')
        genre_id = self.request.query_params.get('genre_id')

        if director_id:
            queryset = queryset.filter(director__id=director_id)
        elif tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        elif genre_id:
            queryset = queryset.filter(genre__id=genre_id)

        # Order randomly and limit results for the 'shelf' effect
        return queryset.order_by('?')[:12]