
from django.shortcuts import render, get_object_or_404
from .models import Camera

def camera_list(request):
    cameras = Camera.objects.all()
    return render(request, 'camera/camera_list.html', {'cameras': cameras})

def camera_detail(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    return render(request, 'camera/camera_detail.html', {'camera': camera})