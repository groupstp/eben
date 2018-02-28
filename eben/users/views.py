import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from django.views.generic import FormView

class AjaxFormMixin(FormView):

    template_name = 'form_ajax.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
        return HttpResponseBadRequest(json.dumps(errors_dict))


class AjaxUpdateFormMixin(AjaxFormMixin, UpdateView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxFormMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxFormMixin, self).post(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('ui',
                       # kwargs={'username': self.request.user.username}
                       )


class UserUpdateView(LoginRequiredMixin, AjaxUpdateFormMixin):

    fields = ['name', 'first_name', 'last_name', 'avatar', 'date_of_birth', 'info', ]

    # we already imported User in the view code above, remember?
    model = User

    template_name = 'users/user_form.html'

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('ui',
                       # kwargs={'username': self.request.user.username}
                       )

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
