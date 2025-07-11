import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .forms import LocationForm, ReviewForm
from .models import Location, Review
from .serializers import LocationSerializer, ReviewSerializer
from .filters import LocationFilter
from rest_framework import viewsets, permissions

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = LocationFilter
    search_fields = ['name', 'description']

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

@login_required
def add_review_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
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
    return render(request, 'locations/review_form.html', {'form': form, 'location': location})


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