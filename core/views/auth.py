import logging
from django.contrib.auth.views import LoginView

logger = logging.getLogger(__name__)


class ERPLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        logger.debug(
            "ERPLoginView.form_valid START user=%s session_key_before=%s incoming_sessionid=%s cookies_before=%s",
            self.request.user,
            self.request.session.session_key,
            self.request.COOKIES.get("sessionid"),
            dict(self.request.COOKIES),
        )
        response = super().form_valid(form)
        logger.debug(
            "ERPLoginView.form_valid END user=%s session_key_after=%s response_cookies=%s",
            self.request.user,
            self.request.session.session_key,
            {k: v.value for k, v in response.cookies.items()},
        )
        return response
