from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path, include
from .views import CustomUserCreateView, CustomUserListView
from . import views
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('log', include(router.urls)),
    path('users/', CustomUserListView.as_view(), name='user-list'),
    path('users/create/', CustomUserCreateView.as_view(), name='user-create'),
    
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('guard/', views.guard_control, name='guard_control'),
    path('main_guard/', views.main_guard_control, name='main_guard_control'),
    path('admin_control/', views.admin_control, name='admin_control'),
    path('director/', views.director_control, name='director_control'),
    path('default/', views.default_page, name='default_page'),
  

]

