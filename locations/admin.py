from django.contrib import admin
from .models import Category, Location, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'latitude', 'longitude', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('location', 'user', 'rating', 'created_at')
    search_fields = ('comment',)
