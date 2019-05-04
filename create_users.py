import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth.hashers import make_password
from paparajotes_y_bellotas.users import models

new_user = models.User(
    username="carbomen",
    email='sample@email.co.uk',
    password=make_password('Sample&Password!'),
    is_active=True,
)
new_user.save()

inva = models.Invitado()
inva.nombre = "Borja"
invb = models.Invitado()
invb.nombre = "Estela"

inva.user = new_user
invb.user = new_user

inva.save()
invb.save()
