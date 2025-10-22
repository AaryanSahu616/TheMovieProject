from rest_framework import generics, status
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Movie, UserReview
from .serializers import MovieSerializer, UserReviewSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


# List all movies OR create new
class MovieTemplateListView(LoginRequiredMixin, ListView):
    model = Movie
    template_name = "TheMovieApp/movies.html"
    context_object_name = "movies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_reviews = UserReview.objects.filter(user=self.request.user)
        # Build a dict {movie_id: review} for fast lookup in template
        context['user_reviews_dict'] = {r.movie_id: r for r in user_reviews}
        return context

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Retrieve, update, delete single movie
class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Add or update a review for a movie
class AddOrUpdateReviewAPIView(generics.GenericAPIView):
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        """
        Create or update a review for a given movie.
        """
        movie = get_object_or_404(Movie, id=movie_id)
        rating = request.data.get("rating")
        review_text = request.data.get("review_text")

        # Validation
        if rating is None or review_text is None:
            return Response({"error": "Both rating and review_text are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has a review for this movie
        existing_review = UserReview.objects.filter(movie=movie, user=request.user).first()

        if existing_review:
            existing_review.rating = int(rating)
            existing_review.review_text = review_text
            existing_review.save()
            return Response({"message": f"Review for '{movie.title}' updated successfully."})
        else:
            UserReview.objects.create(
                movie=movie,
                user=request.user,
                rating=int(rating),
                review_text=review_text,
            )
            return Response({"message": f"Review for '{movie.title}' added successfully."})
