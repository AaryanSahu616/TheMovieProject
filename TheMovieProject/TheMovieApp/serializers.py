# In your app's serializers.py

from rest_framework import serializers
from .models import Director, Genre, Tags, Movie, UserReview

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name', 'birth_date']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name']

# Assuming MovieSerializer and UserReviewSerializer already exist,
# but here are basic versions for completeness:
class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source='director.name', read_only=True)
    genres = GenreSerializer(source='genre', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ['rating', 'review_text'] # Minimal fields for the review post payload