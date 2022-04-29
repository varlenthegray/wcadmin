from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .forms import LoginForm, ProfileForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


class Login(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    template_name = 'users/login.html'
    next_page = 'login'


class Profile(LoginRequiredMixin, generic.UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # Placing the ** before it tells the model to treat form.cleaned_data as a dictionary of keyword arguments
            u = User.objects.filter(pk=kwargs['pk'])
            u.update(**form.cleaned_data)

            if form.password:
                u.set_password(form.password)

            return HttpResponseRedirect('/')
        else:
            return HttpResponse(form.errors.values())
