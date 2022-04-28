from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm


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
