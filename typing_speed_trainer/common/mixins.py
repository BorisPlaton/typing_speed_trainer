from django.conf import settings
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View


class UnauthenticatedMixin(View, SuccessURLAllowedHostsMixin):
    redirect_to: str = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self) -> str:
        """Возвращает ссылку для редиректа."""
        redirect_url = resolve_url(self.request.GET.get('next') or self.redirect_to or settings.LOGIN_REDIRECT_URL)

        self.validate_url(redirect_url)

        return redirect_url if self.is_safe_url(redirect_url) else None

    def validate_url(self, url: str):
        """Проверяет корректная ли ссылка. Если нет, вызывает исключение."""

        if url == self.request.path:
            raise ValueError("Ссылка для редиректа ссылается на текущую страницу: %s" % url)
        elif not url:
            raise ValueError(
                "Укажите атрибут `redirect_to`, `settings.LOGIN_REDIRECT_URL` или параметр запроса `next`."
            )

    def is_safe_url(self, url: str) -> bool:
        """Проверяет безопасная ли ссылка, если да, возвращает True, иначе False."""
        url_is_safe = url_has_allowed_host_and_scheme(
            url=url,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return url_is_safe
