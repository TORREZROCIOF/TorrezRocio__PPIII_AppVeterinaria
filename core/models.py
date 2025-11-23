"""
Models para Sistema Veterinaria
Mapea la base de datos MySQL existente
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# =============================================
# CUSTOM USER MANAGER
# =============================================

class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo Usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario normal"""
        if not email:
            raise ValueError('El usuario debe tener un email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('rol', 'admin')
        extra_fields.setdefault('estado', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


# =============================================
# MODELO: USUARIO (Custom User)
# =============================================

class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de Usuario personalizado que usa email en lugar de username
    Mapea la tabla 'usuarios' de MySQL
    """
    
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('veterinario', 'Veterinario'),
        ('recepcionista', 'Recepcionista'),
    ]
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='recepcionista')
    telefono = models.CharField(max_length=20, null=True, blank=True)
    estado = models.BooleanField(default=True)
    
    # Campos adicionales para Django admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_rol_display()})"
    
    def get_full_name(self):
        return self.nombre
    
    def get_short_name(self):
        return self.nombre.split()[0]


# =============================================
# MODELO: CLIENTE
# =============================================

class Cliente(models.Model):
    """Propietarios de las mascotas"""
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido', 'nombre']
        indexes = [
            models.Index(fields=['dni']),
            models.Index(fields=['telefono']),
        ]
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


# =============================================
# MODELO: MASCOTA
# =============================================

class Mascota(models.Model):
    """Pacientes de la veterinaria"""
    
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Reptil'),
        ('otro', 'Otro'),
    ]
    
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('fallecido', 'Fallecido'),
        ('transferido', 'Transferido'),
    ]
    
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.RESTRICT, 
        related_name='mascotas',
        db_column='cliente_id'
    )
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    raza = models.CharField(max_length=100, null=True, blank=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    foto_url = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    alergias = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mascotas'
        verbose_name = 'Mascota'
        verbose_name_plural = 'Mascotas'
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['especie']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.get_especie_display()})"
    
    @property
    def edad(self):
        """Calcula la edad aproximada de la mascota"""
        if self.fecha_nacimiento:
            today = timezone.now().date()
            edad = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month:
                edad -= 1
            return edad
        return None


# =============================================
# MODELO: CITA
# =============================================

class Cita(models.Model):
    """Turnos y consultas programadas"""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        related_name='citas',
        db_column='mascota_id'
    )
    veterinario = models.ForeignKey(
        Usuario, 
        on_delete=models.RESTRICT, 
        related_name='citas',
        db_column='veterinario_id'
    )
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(null=True, blank=True)
    duracion_minutos = models.IntegerField(default=30)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'citas'
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['fecha_hora']),
            models.Index(fields=['veterinario', 'fecha_hora']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"Cita: {self.mascota.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


# =============================================
# MODELO: CONSULTA
# =============================================

class Consulta(models.Model):
    """Historial médico de consultas"""
    
    id = models.AutoField(primary_key=True)
    cita = models.ForeignKey(
        Cita, 
        on_delete=models.CASCADE, 
        related_name='consultas',
        db_column='cita_id'
    )
    mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        related_name='consultas',
        db_column='mascota_id'
    )
    veterinario = models.ForeignKey(
        Usuario, 
        on_delete=models.RESTRICT, 
        related_name='consultas',
        db_column='veterinario_id'
    )
    fecha_consulta = models.DateTimeField()
    motivo_consulta = models.TextField()
    sintomas = models.TextField(null=True, blank=True)
    diagnostico = models.TextField(null=True, blank=True)
    tratamiento = models.TextField(null=True, blank=True)
    peso_actual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    frecuencia_cardiaca = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    proxima_visita = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'consultas'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-fecha_consulta']
        indexes = [
            models.Index(fields=['mascota', '-fecha_consulta']),
            models.Index(fields=['veterinario']),
        ]
    
    def __str__(self):
        return f"Consulta: {self.mascota.nombre} - {self.fecha_consulta.strftime('%d/%m/%Y')}"


# =============================================
# MODELO: VACUNA
# =============================================

class Vacuna(models.Model):
    """Registro de vacunación"""
    
    id = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        related_name='vacunas',
        db_column='mascota_id'
    )
    nombre_vacuna = models.CharField(max_length=100)
    fecha_aplicacion = models.DateField()
    proxima_dosis = models.DateField(null=True, blank=True)
    veterinario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='vacunas',
        db_column='veterinario_id'
    )
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vacunas'
        verbose_name = 'Vacuna'
        verbose_name_plural = 'Vacunas'
        ordering = ['-fecha_aplicacion']
        indexes = [
            models.Index(fields=['mascota']),
            models.Index(fields=['proxima_dosis']),
        ]
    
    def __str__(self):
        return f"{self.nombre_vacuna} - {self.mascota.nombre}"
    
    @property
    def esta_vencida(self):
        """Verifica si la próxima dosis está vencida"""
        if self.proxima_dosis:
            return self.proxima_dosis < timezone.now().date()
        return False