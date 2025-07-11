from django import forms
from django.shortcuts import redirect, render
from .models import Location, Review
from captcha.fields import CaptchaField

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'category', 'latitude', 'longitude']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']

def create_location_view(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.author = request.user
            location.save()
            return redirect('location-map')
    else:
        form = LocationForm()
    return render(request, 'locations/location_form.html', {'form': form})


