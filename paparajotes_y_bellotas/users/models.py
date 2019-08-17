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
    es_menor = models.BooleanField(_("Es menor"), default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    llegada = models.DateTimeField(_("Llegada"), default=datetime.datetime(2000, 1, 1, 0, 0))
    salida = models.DateTimeField(_("Salida"), default=datetime.datetime(2000, 1, 1, 0, 0))

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.user.username)
