from rest_framework import serializers
from .models import Location, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = '__all__'

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Широта має бути в межах від -90 до 90.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Довгота має бути в межах від -180 до 180.")
        return value

    def get_average_rating(self, obj):
        return obj.average_rating()

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'location', 'user', 'comment', 'rating', 'likes_count', 'dislikes_count', 'created_at']
        read_only_fields = ['user']
