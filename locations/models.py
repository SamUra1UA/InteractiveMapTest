from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        ratings = self.reviews.all().values_list('rating', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 1)
        return 0.0

    def __str__(self):
        return self.name


RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
class Review(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('location', 'user')

    def __str__(self):
        return f"{self.user.username} — {self.rating}/5"
