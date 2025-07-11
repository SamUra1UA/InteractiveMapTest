from django.urls import path, include

from captcha.fields import CaptchaField

from .views import location_detail_view, like_review, dislike_review, map_view

urlpatterns = [
    path('map/', map_view, name='location-map'),
    path('<int:pk>/', location_detail_view, name='location-detail'),
    path('review/<int:review_id>/like/', like_review),
    path('review/<int:review_id>/dislike/', dislike_review),
    path('captcha/', include('captcha.urls')),



]
