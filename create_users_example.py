import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.contrib.auth.hashers import make_password
from paparajotes_y_bellotas.users import models

new_user = models.User(
    username="user",
    email='sample@email.co.uk',
    password=make_password('pass'),
    is_active=True,
)
new_user.save()

inva = models.Invitado()
inva.nombre = "B"
invb = models.Invitado()
invb.nombre = "E"

inva.user = new_user
invb.user = new_user

inva.save()
invb.save()
