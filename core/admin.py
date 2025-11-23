"""
Configuración del Django Admin para Sistema Veterinaria
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Usuario, Cliente, Mascota, Cita, Consulta, Vacuna


# =============================================
# ADMIN: USUARIO
# =============================================

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Admin personalizado para el modelo Usuario"""
    
    list_display = ['email', 'nombre', 'rol', 'telefono', 'estado_badge', 'is_staff']
    list_filter = ['rol', 'estado', 'is_staff', 'is_superuser']
    search_fields = ['nombre', 'email', 'telefono']
    ordering = ['nombre']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'telefono', 'rol')}),
        ('Permisos', {'fields': ('estado', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2', 'rol', 'telefono', 'estado'),
        }),
    )
    
    def estado_badge(self, obj):
        """Muestra un badge de color según el estado"""
        if obj.estado:
            return format_html('<span style="color: green; font-weight: bold;">✓ Activo</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactivo</span>')
    estado_badge.short_description = 'Estado'


# =============================================
# ADMIN: CLIENTE
# =============================================

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para el modelo Cliente"""
    
    list_display = ['nombre_completo', 'dni', 'telefono', 'email', 'total_mascotas', 'estado']
    list_filter = ['estado']
    search_fields = ['nombre', 'apellido', 'dni', 'telefono', 'email']
    ordering = ['apellido', 'nombre']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'dni', 'email', 'telefono')
        }),
        ('Dirección', {
            'fields': ('direccion',)
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    def total_mascotas(self, obj):
        """Cuenta las mascotas del cliente"""
        count = obj.mascotas.count()
        return format_html('<strong>{}</strong>', count)
    total_mascotas.short_description = 'Mascotas'


# =============================================
# ADMIN: MASCOTA
# =============================================

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    """Admin para el modelo Mascota"""
    
    list_display = ['nombre', 'especie', 'raza', 'sexo', 'cliente', 'edad_display', 'peso', 'estado']
    list_filter = ['especie', 'sexo', 'estado', 'fecha_registro']
    search_fields = ['nombre', 'cliente__nombre', 'cliente__apellido', 'raza']
    ordering = ['nombre']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('cliente', 'nombre', 'especie', 'raza', 'sexo')
        }),
        ('Datos Físicos', {
            'fields': ('fecha_nacimiento', 'peso', 'color', 'foto_url')
        }),
        ('Salud', {
            'fields': ('alergias', 'observaciones', 'estado')
        }),
    )
    
    autocomplete_fields = ['cliente']
    
    def edad_display(self, obj):
        """Muestra la edad de la mascota"""
        if obj.edad is not None:
            return f"{obj.edad} año(s)"
        return "-"
    edad_display.short_description = 'Edad'


# =============================================
# ADMIN: CITA
# =============================================

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    """Admin para el modelo Cita"""
    
    list_display = ['fecha_hora', 'mascota', 'veterinario', 'motivo_corto', 'estado_badge', 'duracion_minutos']
    list_filter = ['estado', 'veterinario', 'fecha_hora']
    search_fields = ['mascota__nombre', 'mascota__cliente__nombre', 'mascota__cliente__apellido', 'motivo']
    ordering = ['-fecha_hora']
    date_hierarchy = 'fecha_hora'
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('mascota', 'veterinario', 'fecha_hora', 'duracion_minutos')
        }),
        ('Detalles', {
            'fields': ('motivo', 'estado', 'observaciones')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_cancelacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_creacion']
    autocomplete_fields = ['mascota']
    
    def motivo_corto(self, obj):
        """Muestra el motivo acortado"""
        if len(obj.motivo) > 50:
            return f"{obj.motivo[:50]}..."
        return obj.motivo
    motivo_corto.short_description = 'Motivo'
    
    def estado_badge(self, obj):
        """Badge de color según el estado"""
        colors = {
            'pendiente': '#ffc107',
            'confirmada': '#17a2b8',
            'en_curso': '#007bff',
            'completada': '#28a745',
            'cancelada': '#dc3545',
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'


# =============================================
# ADMIN: CONSULTA
# =============================================

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    """Admin para el modelo Consulta"""
    
    list_display = ['fecha_consulta', 'mascota', 'veterinario', 'diagnostico_corto', 'peso_actual', 'temperatura']
    list_filter = ['veterinario', 'fecha_consulta']
    search_fields = ['mascota__nombre', 'diagnostico', 'tratamiento']
    ordering = ['-fecha_consulta']
    date_hierarchy = 'fecha_consulta'
    
    fieldsets = (
        ('Información General', {
            'fields': ('cita', 'mascota', 'veterinario', 'fecha_consulta')
        }),
        ('Consulta', {
            'fields': ('motivo_consulta', 'sintomas', 'diagnostico', 'tratamiento')
        }),
        ('Signos Vitales', {
            'fields': ('peso_actual', 'temperatura', 'frecuencia_cardiaca')
        }),
        ('Observaciones', {
            'fields': ('observaciones', 'proxima_visita')
        }),
    )
    
    readonly_fields = ['fecha_creacion']
    autocomplete_fields = ['mascota', 'cita']
    
    def diagnostico_corto(self, obj):
        """Muestra el diagnóstico acortado"""
        if obj.diagnostico and len(obj.diagnostico) > 60:
            return f"{obj.diagnostico[:60]}..."
        return obj.diagnostico or "-"
    diagnostico_corto.short_description = 'Diagnóstico'


# =============================================
# ADMIN: VACUNA
# =============================================

@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    """Admin para el modelo Vacuna"""
    
    list_display = ['nombre_vacuna', 'mascota', 'fecha_aplicacion', 'proxima_dosis', 'estado_dosis', 'veterinario']
    list_filter = ['fecha_aplicacion', 'veterinario']
    search_fields = ['nombre_vacuna', 'mascota__nombre', 'mascota__cliente__nombre']
    ordering = ['-fecha_aplicacion']
    date_hierarchy = 'fecha_aplicacion'
    
    fieldsets = (
        ('Información de la Vacuna', {
            'fields': ('mascota', 'nombre_vacuna', 'veterinario')
        }),
        ('Fechas', {
            'fields': ('fecha_aplicacion', 'proxima_dosis')
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
    )
    
    readonly_fields = ['fecha_registro']
    autocomplete_fields = ['mascota']
    
    def estado_dosis(self, obj):
        """Muestra el estado de la próxima dosis"""
        if obj.proxima_dosis:
            if obj.esta_vencida:
                return format_html('<span style="color: red; font-weight: bold;">⚠ Vencida</span>')
            else:
                return format_html('<span style="color: green;">✓ Al día</span>')
        return "-"
    estado_dosis.short_description = 'Estado'


# Configuración del Admin Site
admin.site.site_header = "Administración Veterinaria"
admin.site.site_title = "Veterinaria Admin"
admin.site.index_title = "Panel de Administración"