"""
Serializers para la API REST del Sistema Veterinaria
"""

from rest_framework import serializers
from .models import Usuario, Cliente, Mascota, Cita, Consulta, Vacuna


# =============================================
# SERIALIZER: USUARIO
# =============================================

class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    
    password = serializers.CharField(write_only=True, required=False)
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'nombre', 'email', 'password', 'rol', 'rol_display',
            'telefono', 'estado', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Crear usuario con password hasheado"""
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """Actualizar usuario, hashear password si se proporciona"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


# =============================================
# SERIALIZER: CLIENTE
# =============================================

class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cliente"""
    
    nombre_completo = serializers.ReadOnlyField()
    total_mascotas = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'apellido', 'nombre_completo', 'dni',
            'email', 'telefono', 'direccion', 'estado', 'total_mascotas'
        ]
        read_only_fields = ['id']
    
    def get_total_mascotas(self, obj):
        """Contar las mascotas activas del cliente"""
        return obj.mascotas.filter(estado='activo').count()


# =============================================
# SERIALIZER: MASCOTA
# =============================================

class MascotaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Mascota"""
    
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    cliente_telefono = serializers.CharField(source='cliente.telefono', read_only=True)
    especie_display = serializers.CharField(source='get_especie_display', read_only=True)
    sexo_display = serializers.CharField(source='get_sexo_display', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    edad = serializers.ReadOnlyField()
    
    class Meta:
        model = Mascota
        fields = [
            'id', 'cliente', 'cliente_nombre', 'cliente_telefono',
            'nombre', 'especie', 'especie_display', 'raza', 
            'sexo', 'sexo_display', 'fecha_nacimiento', 'edad',
            'peso', 'color', 'foto_url', 'estado', 'estado_display',
            'alergias', 'observaciones', 'fecha_registro'
        ]
        read_only_fields = ['id', 'fecha_registro']


# =============================================
# SERIALIZER: CITA
# =============================================

class CitaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Cita"""
    
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    mascota_especie = serializers.CharField(source='mascota.get_especie_display', read_only=True)
    cliente_nombre = serializers.CharField(source='mascota.cliente.nombre_completo', read_only=True)
    cliente_telefono = serializers.CharField(source='mascota.cliente.telefono', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Cita
        fields = [
            'id', 'mascota', 'mascota_nombre', 'mascota_especie',
            'cliente_nombre', 'cliente_telefono',
            'veterinario', 'veterinario_nombre',
            'fecha_hora', 'motivo', 'estado', 'estado_display',
            'observaciones', 'duracion_minutos',
            'fecha_creacion', 'fecha_cancelacion'
        ]
        read_only_fields = ['id', 'fecha_creacion']
    
    def validate_fecha_hora(self, value):
        """Validar que la fecha de la cita sea futura"""
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de la cita no puede ser en el pasado")
        return value


# =============================================
# SERIALIZER: CONSULTA
# =============================================

class ConsultaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Consulta"""
    
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    mascota_especie = serializers.CharField(source='mascota.get_especie_display', read_only=True)
    cliente_nombre = serializers.CharField(source='mascota.cliente.nombre_completo', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.nombre', read_only=True)
    
    class Meta:
        model = Consulta
        fields = [
            'id', 'cita', 'mascota', 'mascota_nombre', 'mascota_especie',
            'cliente_nombre', 'veterinario', 'veterinario_nombre',
            'fecha_consulta', 'motivo_consulta', 'sintomas',
            'diagnostico', 'tratamiento', 'peso_actual', 'temperatura',
            'frecuencia_cardiaca', 'observaciones', 'proxima_visita',
            'fecha_creacion'
        ]
        read_only_fields = ['id', 'fecha_creacion']


# =============================================
# SERIALIZER: VACUNA
# =============================================

class VacunaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Vacuna"""
    
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='mascota.cliente.nombre_completo', read_only=True)
    cliente_telefono = serializers.CharField(source='mascota.cliente.telefono', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.nombre', read_only=True)
    esta_vencida = serializers.ReadOnlyField()
    dias_para_refuerzo = serializers.SerializerMethodField()
    
    class Meta:
        model = Vacuna
        fields = [
            'id', 'mascota', 'mascota_nombre', 'cliente_nombre', 'cliente_telefono',
            'nombre_vacuna', 'fecha_aplicacion', 'proxima_dosis',
            'veterinario', 'veterinario_nombre', 'observaciones',
            'fecha_registro', 'esta_vencida', 'dias_para_refuerzo'
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def get_dias_para_refuerzo(self, obj):
        """Calcular días restantes para el refuerzo"""
        if obj.proxima_dosis:
            from django.utils import timezone
            delta = obj.proxima_dosis - timezone.now().date()
            return delta.days
        return None


# =============================================
# SERIALIZERS RESUMIDOS (para listados)
# =============================================

class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listados de clientes"""
    total_mascotas = serializers.SerializerMethodField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'apellido', 'telefono', 'total_mascotas']
    
    def get_total_mascotas(self, obj):
        return obj.mascotas.filter(estado='activo').count()


class MascotaListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listados de mascotas"""
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    
    class Meta:
        model = Mascota
        fields = ['id', 'nombre', 'especie', 'raza', 'cliente_nombre']


class CitaListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listados de citas"""
    mascota_nombre = serializers.CharField(source='mascota.nombre', read_only=True)
    veterinario_nombre = serializers.CharField(source='veterinario.nombre', read_only=True)
    
    class Meta:
        model = Cita
        fields = ['id', 'fecha_hora', 'mascota_nombre', 'veterinario_nombre', 'estado']