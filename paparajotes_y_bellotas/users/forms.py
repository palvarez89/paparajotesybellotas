from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.forms import ModelForm, CharField

from paparajotes_y_bellotas.users import models


User = get_user_model()


class UserChangeForm(ModelForm):

    class Meta:
        model = User
        fields = ["mensaje", "firma"]

class BaseInvitadoFormset(ModelForm):

    nombre = CharField(disabled=True)
    class Meta:
        model = models.Invitado
        fields = []

    def add_fields(self, form, index):
        super(BaseInvitadoFormset, self).add_fields(form, index)


InvitadoFormset = inlineformset_factory(
    models.User,
    models.Invitado,
    form=BaseInvitadoFormset,
    fields=[
        "nombre",
        "asiste",
        "autobus",
        "llegada",
        "salida",
        "lunes16velero",
        "martes17playa",
        "miercoles18comida",
        "jueves19playa",
    ],
    extra=0,
    can_delete=False
)

class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
