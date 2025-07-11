from django.urls import path, include
from . import views
from .views import autocomplete_locations

urlpatterns = [
    path('map/', views.map_view, name='location-map'),
    path('export/json/', views.export_locations_json, name='export_json'),
    path('export/csv/', views.export_locations_csv, name='export_csv'),
    path('add/', views.create_location_view, name='add-location'),
    path('<int:pk>/', views.location_detail_view, name='location-detail'),
    path('<int:pk>/review/', views.add_review_view, name='add-review'),
    path('review/<int:review_id>/like/', views.like_review, name='like-review'),
    path('review/<int:review_id>/dislike/', views.dislike_review, name='dislike-review'),
    path('captcha/', include('captcha.urls')),
    path('<int:pk>/edit/', views.edit_location_view, name='edit-location'),
    path('<int:pk>/delete/', views.delete_location_view, name='delete-location'),
    path('autocomplete/', autocomplete_locations, name='autocomplete'),

]
