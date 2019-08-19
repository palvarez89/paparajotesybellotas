from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.db import transaction

from paparajotes_y_bellotas.users import models
from paparajotes_y_bellotas.users import forms
from paparajotes_y_bellotas.users.forms import UserChangeForm, InvitadoFormset

User = get_user_model()

class StaffRequiredMixin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(StaffRequiredMixin, self).as_view(*args, **kwargs)
        return staff_member_required(view)


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(StaffRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm

    def get_context_data(self, **kwargs):
        data = super(UserUpdateView, self).get_context_data(**kwargs)
        user = self.get_object()
        if self.request.POST:
            data['invitados'] = InvitadoFormset(self.request.POST, instance=user)
        else:
            data['invitados'] = forms.InvitadoFormset(instance=user)
        return data

    def get_success_url(self):
        return reverse("users:update")

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        context = self.get_context_data()
        invitados = context['invitados']
        if invitados.is_valid():
            invitados.instance = self.object
            invitados.save()
            parent_valid = super(UserUpdateView, self).form_valid(form)
            if parent_valid:
                messages.success(self.request, _("Datos actualizados correctamente"))
                return parent_valid
        else:
            messages.error(self.request, _("Fallo al enviar los datos, revisa el formulario"))
            return self.render_to_response(self.get_context_data(form=form))


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:update")


user_redirect_view = UserRedirectView.as_view()
