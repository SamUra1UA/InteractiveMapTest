from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .forms import create_location_view
from .views import LocationViewSet, export_locations_json, export_locations_csv, edit_location_view, \
    delete_location_view, add_review_view, ReviewViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('export/json/', export_locations_json, name='export_json'),
    path('export/csv/', export_locations_csv, name='export_csv'),
    path('<int:pk>/edit/', edit_location_view, name='edit-location'),
    path('<int:pk>/delete/', delete_location_view, name='delete-location'),
    path('<int:pk>/review/', add_review_view, name='add-review'),
    path('add/', create_location_view, name='add-location'),
]
