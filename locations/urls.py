from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from rest_framework.routers import DefaultRouter

from . import views
from captcha.fields import CaptchaField

from .views import LocationViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')

urlpatterns = [
    path('api/', include(router.urls)),
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


]
