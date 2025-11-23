"""
Views para Sistema Veterinaria
Incluye autenticación, dashboard y API endpoints
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .forms import CitaForm

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario, Cliente, Mascota, Cita, Consulta, Vacuna
from .serializers import (
    UsuarioSerializer, ClienteSerializer, MascotaSerializer,
    CitaSerializer, ConsultaSerializer, VacunaSerializer
)


# =============================================
# VISTAS DE AUTENTICACIÓN (Template-based)
# =============================================

def login_view(request):
    """Vista de login tradicional con templates"""
    
    # Si ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticar usuario
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.estado:  # Verificar que el usuario esté activo
                login(request, user)
                messages.success(request, f'Bienvenido, {user.nombre}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Tu cuenta está desactivada.')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    """Vista de logout"""
    nombre = request.user.nombre
    logout(request)
    messages.info(request, f'Hasta pronto, {nombre}!')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard principal del sistema"""
    
    # Obtener fecha actual
    hoy = timezone.now().date()
    
    # Estadísticas generales
    stats = {
        'total_clientes': Cliente.objects.filter(estado=True).count(),
        'total_mascotas': Mascota.objects.filter(estado='activo').count(),
        'citas_hoy': Cita.objects.filter(
            fecha_hora__date=hoy,
            estado__in=['pendiente', 'confirmada']
        ).count(),
        'consultas_mes': Consulta.objects.filter(
            fecha_consulta__month=hoy.month,
            fecha_consulta__year=hoy.year
        ).count(),
    }
    
    # Citas de hoy
    citas_hoy = Cita.objects.filter(
        fecha_hora__date=hoy
    ).select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).order_by('fecha_hora')[:10]
    
    # Próximas citas
    proximas_citas = Cita.objects.filter(
        fecha_hora__gte=timezone.now(),
        estado__in=['pendiente', 'confirmada']
    ).select_related(
        'mascota', 'mascota__cliente', 'veterinario'
    ).order_by('fecha_hora')[:5]
    
    # Vacunas próximas a vencer (próximos 30 días)
    fecha_limite = hoy + timedelta(days=30)
    vacunas_proximas = Vacuna.objects.filter(
        proxima_dosis__gte=hoy,
        proxima_dosis__lte=fecha_limite
    ).select_related(
        'mascota', 'mascota__cliente'
    ).order_by('proxima_dosis')[:5]
    
    # Distribución de mascotas por especie
    mascotas_por_especie = Mascota.objects.filter(
        estado='activo'
    ).values('especie').annotate(
        total=Count('id')
    ).order_by('-total')
    
    context = {
        'stats': stats,
        'citas_hoy': citas_hoy,
        'proximas_citas': proximas_citas,
        'vacunas_proximas': vacunas_proximas,
        'mascotas_por_especie': mascotas_por_especie,
        'usuario': request.user,
    }
    
    return render(request, 'dashboard.html', context)


# =============================================
# API VIEWS (REST Framework)
# =============================================

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API endpoint para login con JWT
    POST /api/login/
    Body: {"email": "...", "password": "..."}
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=email, password=password)
    
    if user is not None:
        if not user.estado:
            return Response(
                {'error': 'Usuario desactivado'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'nombre': user.nombre,
                'email': user.email,
                'rol': user.rol,
            }
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Credenciales inválidas'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """
    API endpoint para logout (blacklist del refresh token)
    POST /api/logout/
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    """
    API endpoint para obtener datos del usuario actual
    GET /api/me/
    """
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)


# =============================================
# VIEWSETS PARA CRUD COMPLETO
# =============================================

class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar según permisos del usuario"""
        if self.request.user.rol == 'admin':
            return Usuario.objects.all()
        return Usuario.objects.filter(id=self.request.user.id)


class ClienteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de clientes"""
    queryset = Cliente.objects.filter(estado=True)
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'apellido', 'dni', 'telefono']
    ordering_fields = ['apellido', 'nombre']
    
    @action(detail=True, methods=['get'])
    def mascotas(self, request, pk=None):
        """Obtener todas las mascotas de un cliente"""
        cliente = self.get_object()
        mascotas = cliente.mascotas.filter(estado='activo')
        serializer = MascotaSerializer(mascotas, many=True)
        return Response(serializer.data)


class MascotaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de mascotas"""
    queryset = Mascota.objects.filter(estado='activo')
    serializer_class = MascotaSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre', 'cliente__nombre', 'cliente__apellido']
    filterset_fields = ['especie', 'sexo', 'cliente']
    
    @action(detail=True, methods=['get'])
    def historial(self, request, pk=None):
        """Obtener historial médico completo de una mascota"""
        mascota = self.get_object()
        
        # Consultas
        consultas = mascota.consultas.all().order_by('-fecha_consulta')[:10]
        consultas_data = ConsultaSerializer(consultas, many=True).data
        
        # Vacunas
        vacunas = mascota.vacunas.all().order_by('-fecha_aplicacion')
        vacunas_data = VacunaSerializer(vacunas, many=True).data
        
        # Citas
        citas = mascota.citas.all().order_by('-fecha_hora')[:5]
        citas_data = CitaSerializer(citas, many=True).data
        
        return Response({
            'mascota': MascotaSerializer(mascota).data,
            'consultas': consultas_data,
            'vacunas': vacunas_data,
            'citas': citas_data,
        })


class CitaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de citas"""
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['estado', 'veterinario', 'mascota']
    ordering_fields = ['fecha_hora']
    
    def get_queryset(self):
        """Filtrar citas según rol del usuario"""
        queryset = Cita.objects.all()
        
        # Si es veterinario, solo sus citas
        if self.request.user.rol == 'veterinario':
            queryset = queryset.filter(veterinario=self.request.user)
        
        # Filtrar por fecha si se proporciona
        fecha = self.request.query_params.get('fecha', None)
        if fecha:
            queryset = queryset.filter(fecha_hora__date=fecha)
        
        return queryset.select_related('mascota', 'mascota__cliente', 'veterinario')
    
    @action(detail=False, methods=['get'])
    def hoy(self, request):
        """Obtener citas de hoy"""
        hoy = timezone.now().date()
        citas = self.get_queryset().filter(fecha_hora__date=hoy)
        serializer = self.get_serializer(citas, many=True)
        return Response(serializer.data)


class ConsultaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de consultas médicas"""
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['mascota', 'veterinario']
    ordering_fields = ['fecha_consulta']
    
    def perform_create(self, serializer):
        """Asignar veterinario automáticamente al crear consulta"""
        serializer.save(veterinario=self.request.user)


class VacunaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de vacunas"""
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['mascota']
    ordering_fields = ['fecha_aplicacion']
    
    @action(detail=False, methods=['get'])
    def proximas(self, request):
        """Obtener vacunas próximas a vencer"""
        hoy = timezone.now().date()
        fecha_limite = hoy + timedelta(days=30)
        
        vacunas = self.get_queryset().filter(
            proxima_dosis__gte=hoy,
            proxima_dosis__lte=fecha_limite
        ).select_related('mascota', 'mascota__cliente')
        
        serializer = self.get_serializer(vacunas, many=True)
        return Response(serializer.data)

# --------------------------
# CRUD CLIENTES
# --------------------------

@login_required
def cliente_listar(request):
    clientes = Cliente.objects.filter(estado=True)
    return render(request, 'clientes/listar.html', {'clientes': clientes})


@login_required
def cliente_crear(request):
    if request.method == "POST":
        Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            dni=request.POST.get('dni'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            estado=True
        )

        messages.success(request, "Cliente creado correctamente")
        return redirect('cliente_listar')

    return render(request, 'clientes/crear.html')


@login_required
def cliente_editar(request, id):
    cliente = Cliente.objects.get(id=id)

    if request.method == "POST":
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.dni = request.POST.get('dni')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.save()

        messages.success(request, "Cliente actualizado correctamente")
        return redirect('cliente_listar')

    return render(request, 'clientes/editar.html', {'cliente': cliente})



@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.estado = False
    cliente.save()
    messages.success(request, "Cliente eliminado correctamente")
    return redirect('cliente_listar')

@login_required
def usuario_listar(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})


@login_required
def usuario_crear(request):
    if request.method == "POST":
        Usuario.objects.create(
            nombre=request.POST['nombre'],
            email=request.POST['email'],
            password=request.POST['password'],
            rol=request.POST['rol'],
            estado=True
        )
        messages.success(request, "Usuario creado correctamente")
        return redirect('usuario_listar')

    return render(request, 'usuarios/crear.html')


@login_required
def usuario_editar(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    if request.method == "POST":
        usuario.nombre = request.POST['nombre']
        usuario.email = request.POST['email']
        usuario.rol = request.POST['rol']
        usuario.estado = 'estado' in request.POST
        usuario.save()

        messages.success(request, "Usuario actualizado correctamente")
        return redirect('usuario_listar')

    return render(request, 'usuarios/editar.html', {'usuario': usuario})



@login_required
def mascota_listar(request):
    mascotas = Mascota.objects.select_related("cliente").all()
    return render(request, "mascotas/listar.html", {"mascotas": mascotas})


@login_required
def mascota_crear(request):
    clientes = Cliente.objects.all()

    if request.method == "POST":
        Mascota.objects.create(
            cliente_id=request.POST["cliente"],
            nombre=request.POST["nombre"],
            especie=request.POST["especie"],
            raza=request.POST.get("raza"),
            sexo=request.POST["sexo"],
            fecha_nacimiento=request.POST.get("fecha_nacimiento"),
            peso=request.POST.get("peso") or None,
            color=request.POST.get("color"),
            foto_url=request.POST.get("foto_url"),
            estado=request.POST["estado"],
            alergias=request.POST.get("alergias"),
            observaciones=request.POST.get("observaciones"),
        )
        messages.success(request, "Mascota creada correctamente")
        return redirect("mascota_listar")

    return render(request, "mascotas/crear.html", {"clientes": clientes})


@login_required
def mascota_editar(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    clientes = Cliente.objects.all()

    if request.method == "POST":
        mascota.cliente_id = request.POST["cliente"]
        mascota.nombre = request.POST["nombre"]
        mascota.especie = request.POST["especie"]
        mascota.raza = request.POST.get("raza")
        mascota.sexo = request.POST["sexo"]
        mascota.fecha_nacimiento = request.POST.get("fecha_nacimiento")
        mascota.peso = request.POST.get("peso") or None
        mascota.color = request.POST.get("color")
        mascota.foto_url = request.POST.get("foto_url")
        mascota.estado = request.POST["estado"]
        mascota.alergias = request.POST.get("alergias")
        mascota.observaciones = request.POST.get("observaciones")

        mascota.save()

        messages.success(request, "Mascota actualizada correctamente")
        return redirect("mascota_listar")

    return render(request, "mascotas/editar.html", {"mascota": mascota, "clientes": clientes})


@login_required
def mascota_eliminar(request, mascota_id):
    mascota = get_object_or_404(Mascota, pk=mascota_id)
    mascota.delete()
    messages.success(request, "Mascota eliminada correctamente")
    return redirect("mascota_listar")

@login_required
def cita_listar(request):
    citas = Cita.objects.select_related('mascota', 'veterinario').all()
    return render(request, 'citas/listar.html', {'citas': citas})

def cita_crear(request):
    mascotas = Mascota.objects.filter(estado="activo").select_related("cliente")
    veterinarios = Usuario.objects.filter(rol="veterinario")

    if request.method == "POST":
        mascota_id = request.POST.get("mascota")
        veterinario_id = request.POST.get("veterinario")
        fecha_hora = request.POST.get("fecha_hora")
        motivo = request.POST.get("motivo")
        observaciones = request.POST.get("observaciones")
        duracion_minutos = request.POST.get("duracion_minutos") or 30

        if not mascota_id or not veterinario_id or not fecha_hora or not motivo:
            messages.error(request, "Todos los campos obligatorios deben completarse.")
            return redirect("cita_crear")

        Cita.objects.create(
            mascota_id=mascota_id,
            veterinario_id=1,
            fecha_hora=fecha_hora,
            motivo=motivo,
            estado=True,
            observaciones=observaciones,
            duracion_minutos=duracion_minutos,
        )

        messages.success(request, "Cita creada correctamente.")
        return redirect("cita_listar")

    return render(request, "citas/crear.html", {
        "mascotas": mascotas,
        "veterinarios": veterinarios,
    })

    return render(request, 'citas/crear.html', {'form': form})

@login_required
def cita_editar(request, id):
    cita = get_object_or_404(Cita, id=id)

    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita actualizada correctamente")
            return redirect('cita_listar')
    else:
        form = CitaForm(instance=cita)

    return render(request, 'citas/editar.html', {'form': form})

@login_required
def cita_eliminar(request, id):
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    messages.success(request, "Cita eliminada")
    return redirect('cita_listar')

