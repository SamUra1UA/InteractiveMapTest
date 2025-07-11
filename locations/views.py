import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from api.forms import ReviewForm
from api.models import Review, Location

API_BASE = 'http://localhost:8000/api/'

@login_required
def location_detail_view(request, pk):
    # Отримуємо дані локації через ORM
    location = get_object_or_404(Location, pk=pk)

    # Отримуємо відгуки через ORM
    reviews = Review.objects.filter(location=location)

    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.location = location
                review.save()
                return redirect('location-detail', pk=pk)
        else:
            form = ReviewForm()

    return render(request, 'locations/location_detail.html', {
        'location': location,
        'reviews': reviews,
        'form': form
    })


def map_view(request):
    query = request.GET.get('q', '')
    params = {'search': query} if query else {}
    response = requests.get(f'{API_BASE}locations/', params=params)
    locations = response.json() if response.status_code == 200 else []

    return render(request, 'map.html', {'locations': locations})

@require_POST
@login_required
def like_review(request, review_id):
    token = request.session.get("auth_token")
    headers = {"Authorization": f"Token {token}"} if token else {}

    res = requests.post(f'{API_BASE}review/{review_id}/like/', headers=headers)
    return JsonResponse(res.json(), status=res.status_code)


@require_POST
@login_required
def dislike_review(request, review_id):
    token = request.session.get("auth_token")
    headers = {"Authorization": f"Token {token}"} if token else {}

    res = requests.post(f'{API_BASE}review/{review_id}/dislike/', headers=headers)
    return JsonResponse(res.json(), status=res.status_code)
