from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Evento(models.Model):
    DEPORTES = [
        ('futbol', 'Fútbol'),
        ('baloncesto', 'Baloncesto'),
        ('voleibol', 'Voleibol'),
        ('tenis', 'Tenis'),
        ('natacion', 'Natación'),
        ('atletismo', 'Atletismo'),
        # Agrega más deportes si lo deseas
    ]
    NIVELES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    deporte = models.CharField(max_length=20, choices=DEPORTES)
    lugar = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    cupos = models.PositiveIntegerField(default=20)
    nivel = models.CharField(max_length=20, choices=NIVELES, default='basico')
    observaciones = models.TextField(blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
