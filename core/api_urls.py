from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet, ClienteViewSet, MascotaViewSet,
    CitaViewSet, ConsultaViewSet, VacunaViewSet,
    api_login, api_logout, api_me
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'mascotas', MascotaViewSet)
router.register(r'citas', CitaViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'vacunas', VacunaViewSet)

urlpatterns = [
    # Endpoints de autenticación API (JWT)
    path('login/', api_login, name='api_login'),
    path('logout/', api_logout, name='api_logout'),
    path('me/', api_me, name='api_me'),

    # Todos los CRUD REST automáticos
    path('', include(router.urls)),
]
