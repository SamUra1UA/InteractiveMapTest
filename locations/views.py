from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Location, Review
from .serializers import LocationSerializer, ReviewSerializer
from .filters import LocationFilter
from django.http import JsonResponse, HttpResponse
import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LocationForm
from .forms import ReviewForm
from .models import Review
from django.views.decorators.http import require_POST
from django.db.models import Q

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = LocationFilter
    search_fields = ['name', 'description']

def export_locations_json(request):
    data = list(Location.objects.values())
    return JsonResponse(data, safe=False)

def export_locations_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="locations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Latitude', 'Longitude', 'Category'])

    for loc in Location.objects.all():
        writer.writerow([loc.name, loc.description, loc.latitude, loc.longitude, loc.category.name if loc.category else ''])

    return response



@login_required
def create_location_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)  # не зберігаємо поки
            location.author = request.user      # ставимо автора
            location.save()                     # тепер зберігаємо
            return redirect('location-map')
    else:
        form = LocationForm()
    return render(request, 'locations/location_form.html', {'form': form})



def autocomplete_locations(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        locations = Location.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))[:5]
        results = [{'id': loc.id, 'name': loc.name} for loc in locations]

    return JsonResponse({'results': results})


def location_detail_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    reviews = location.reviews.select_related('user')
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




@login_required
def add_review_view(request, pk):
    location = Location.objects.get(pk=pk)
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
    return render(request, 'locations/review_form.html', {'form': form, 'location': location}), redirect('location-detail', pk=pk)


from django.db.models import Q

def map_view(request):
    query = request.GET.get('q')
    locations = Location.objects.all()
    if query:
        locations = locations.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'map.html', {'locations': locations})


@require_POST
@login_required
def like_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    user = request.user
    if user in review.likes.all():
        review.likes.remove(user)
        liked = False
    else:
        review.likes.add(user)
        review.dislikes.remove(user)
        liked = True
    return JsonResponse({'likes': review.likes.count(), 'dislikes': review.dislikes.count(), 'liked': liked})

@require_POST
@login_required
def dislike_review(request, review_id):
    review = Review.objects.get(pk=review_id)
    user = request.user
    if user in review.dislikes.all():
        review.dislikes.remove(user)
        disliked = False
    else:
        review.dislikes.add(user)
        review.likes.remove(user)
        disliked = True
    return JsonResponse({'likes': review.likes.count(), 'dislikes': review.dislikes.count(), 'disliked': disliked})

@login_required
def edit_location_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('location-detail', pk=pk)
    else:
        form = LocationForm(instance=location)
    return render(request, 'locations/edit_location.html', {'form': form, 'location': location})

@login_required
def delete_location_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('location-map')  # або будь-яка інша сторінка
    return render(request, 'locations/confirm_delete.html', {'location': location})