from django.urls import path, include
from .views import (
    login_view, logout_view, dashboard_view
)
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ClienteViewSet, MascotaViewSet,
    CitaViewSet, ConsultaViewSet, VacunaViewSet,
    api_login, api_logout, api_me, usuario_listar, usuario_crear, usuario_editar,
    cliente_listar, cliente_crear, cliente_editar,
    mascota_listar, mascota_crear, mascota_editar, mascota_eliminar,
    cita_eliminar, cita_listar, cita_crear, cita_editar,
)

# Router para API
router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)
router.register('clientes', ClienteViewSet)
router.register('mascotas', MascotaViewSet)
router.register('citas', CitaViewSet)
router.register('consultas', ConsultaViewSet)
router.register('vacunas', VacunaViewSet)

urlpatterns = [
    # Vistas HTML
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # API simple JWT login/logout/me
    path('api/login/', api_login, name='api_login'),
    path('api/logout/', api_logout, name='api_logout'),
    path('api/me/', api_me, name='api_me'),

    # API REST Framework
    path('api/', include(router.urls)),

    # Usuarios
    path('usuarios/', usuario_listar, name='usuario_listar'),
    path('usuarios/crear/', usuario_crear, name='usuario_crear'),
    path('usuarios/editar/<int:id>/', usuario_editar, name='usuario_editar'),

    # Clientes
    path('clientes/', cliente_listar, name='cliente_listar'),
    path('clientes/crear/', cliente_crear, name='cliente_crear'),
    path('clientes/editar/<int:id>/', cliente_editar, name='cliente_editar'),

    # MASCOTAS
    path('mascotas/', mascota_listar, name='mascota_listar'),
    path('mascotas/crear/', mascota_crear, name='mascota_crear'),
    path('mascotas/editar/<int:id>/', mascota_editar, name='mascota_editar'),

    # --- CITAS ---
    path('citas/', cita_listar, name='cita_listar'),
    path('citas/crear/', cita_crear, name='cita_crear'),
    path('citas/editar/<int:id>/', cita_editar, name='cita_editar'),
    path('citas/eliminar/<int:id>/', cita_eliminar, name='cita_eliminar'),

]
