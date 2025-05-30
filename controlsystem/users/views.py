from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from .serializers import CustomUserSerializer
from rest_framework import generics
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from camera.models import Camera

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    
class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Редирект в зависимости от роли
            if user.role == 'guard':
                return redirect('guard_control')
            elif user.role == 'main_guard':
                return redirect('main_guard_control')
            elif user.role == 'admin':
                return redirect('admin_control')
            elif user.role == 'director':
                return redirect('director_control')
            else:
                # Если роль неизвестна, редирект куда-то по умолчанию
                return redirect('default_page')
        else:
            error = "Неверный логин или пароль"

    return render(request, 'users/login.html', {'error': error})


@login_required
def guard_control(request):
    cameras = Camera.objects.all()
    # Если у тебя есть парковки, добавь их тоже:
    # from parking.models import Parking
    # parkings = Parking.objects.all()
    # return render(request, 'users/guard_control.html', {'cameras': cameras, 'parkings': parkings})

    return render(request, 'users/guard_control.html', {'cameras': cameras})

@login_required
def main_guard_control(request):
    return render(request, 'users/main_guard_control.html')

@login_required
def admin_control(request):
    return render(request, 'users/admin_control.html')

@login_required
def director_control(request):
    return render(request, 'users/director_control.html')

@login_required
def default_page(request):
    return render(request, 'users/default_page.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def journal_view(request, employee):
    menu_template = 'users/guard_menu.html'
    visit_logs = VisitLog.objects.all().select_related('visitor', 'car', 'parking').order_by('-entry_time')

    formatted_logs = []
    for log in visit_logs:
        formatted_logs.append({
            'visitor_name': log.visitor.get_full_name() if log.visitor else '',
            'visitor_position': getattr(log.visitor, 'position', ''),
            'visitor_organization': getattr(log.visitor, 'organization', ''),
            'car_info': f"{log.car.brand} {log.car.model} ({log.car.license_plate})" if log.car else "Нет данных",
            'parking_name': log.parking.name if log.parking else '',
            'entry_time': log.entry_time.strftime('%d.%m.%Y %H:%M'),
            'exit_time': log.exit_time.strftime('%d.%m.%Y %H:%M') if log.exit_time else '',
            'entry_photo': log.entry_photo.url if hasattr(log, 'entry_photo') and log.entry_photo else '',
            'exit_photo': log.exit_photo.url if hasattr(log, 'exit_photo') and log.exit_photo else '',
        })

    return render(request, 'main/guard_journal.html', {
        'visit_logs': formatted_logs,
        'menu_template': menu_template,
        'employee': employee
    })
