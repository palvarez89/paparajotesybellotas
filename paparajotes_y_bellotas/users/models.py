from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, BooleanField, Model, ForeignKey, DateTimeField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
import datetime


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    mensaje = models.CharField(_("Mensaje"), blank=True, max_length=255)
    firma = models.CharField(_("Firma"), blank=True, max_length=40)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Invitado(Model):
    nombre = models.CharField(_("Nombre"), blank=True, max_length=255)
    asiste = models.BooleanField(_("Confirmada asistencia"), default=False)
    autobus = models.BooleanField(_("Autobus"), default=False)
    notas = models.CharField(_("Notas"), blank=True, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    llegada = models.DateField(_("Llegada"), default=datetime.date(2019, 9, 21))
    salida = models.DateField(_("Salida"), default=datetime.date(2019, 9, 21))

    lunes16velero = models.BooleanField(_("lunes16velero"), default=False)
    martes17playa = models.BooleanField(_("martes17playa"), default=False)
    miercoles18comida = models.BooleanField(_("miercoles18comida"), default=False)
    jueves19playa = models.BooleanField(_("jueves19playa"), default=False)

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.user.username)
