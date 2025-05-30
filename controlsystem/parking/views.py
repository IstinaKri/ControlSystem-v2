from django.shortcuts import render, get_object_or_404
from .models import Parking

def parking_list(request):
    parkings = Parking.objects.all()
    return render(request, 'parking/parking_list.html', {'parkings': parkings})

def parking_detail(request, pk):
    parking = get_object_or_404(Parking, pk=pk)
    return render(request, 'parking/parking_detail.html', {'parking': parking})