from rest_framework import serializers
from .models import Movie, UserReview

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = "__all__"
        read_only_fields = ["user", "movie"]
