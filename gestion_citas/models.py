from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

# Modelo Especialidad
class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    
     #Ajuste a la tabla y modelos => 's o => oes
    class Meta:
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"
        ordering = ['nombre'] #ordenar por nombre

    def __str__(self):
        return self.nombre

# Modelo Paciente (Relación 1:1 con el Usuario para autenticación)
class Paciente(models.Model):
    # Usamos la FK como PK para implementar la relación 1:1, extendiendo al User
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fecha_nacimiento = models.DateField(default="2000-01-01")
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    
     #Ajuste a la tabla y modelos => 's o => oes
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['usuario__first_name'] #ordenar por nombre

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}" 

# Modelo Medico (Relación 1:1 con el Usuario para autenticación)
class Medico(models.Model):
    # Usamos la FK como PK para implementar la relación 1:1, extendiendo al User
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) 
    matricula = models.CharField(max_length=50, unique=True )
    telefono = models.CharField(max_length=20)
    # Relación Muchos a Muchos con Especialidad
    especialidades = models.ManyToManyField(Especialidad) 
    
    #Ajuste a la tabla y modelos => 's o => oes
    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"
        ordering = ['usuario__first_name'] #ordenar por nombre

    def __str__(self):
        nombres = f"{self.usuario.first_name}" if self.usuario.first_name else ""
        apellidos = f" {self.usuario.last_name}" if self.usuario.last_name else ""
        especialidades = ", ".join(e.nombre for e in self.especialidades.all()) if self.pk else ""
        if especialidades:
            return f"Dr(a). {nombres}{apellidos} ({especialidades})"
        return f"Dr(a). {nombres}{apellidos}"

# Modelo Cita
class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField() # Un solo campo para fecha y hora
    motivo = models.TextField()
    estado = models.CharField(max_length=20, default='Pendiente')
    
    #Ajuste a la tabla y modelos => 's o =>
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['estado'] #ordenar por nombre

    # Relación Uno a Muchos (1:N) con Paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas_paciente')
    # Relación Uno a Muchos (1:N) con Medico
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas_medico')
    
    def __str__(self):
        return f"Cita {self.id_cita} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M')}"