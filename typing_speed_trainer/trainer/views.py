from django.views.generic import TemplateView

from account.models import User
from common.mixins import ResultsFormattingMixin
from trainer.utils.cache_results import AllUserResultsMixin


class TypingTrainer(TemplateView, ResultsFormattingMixin, AllUserResultsMixin):
    """Страница с тренажером скорости печати."""

    template_name = 'trainer/typing_trainer.html'
    user_models = User.objects.select_related('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_users_results'] = self.get_formatted_date_end_results(
            self.get_last_cached_results(10, with_users=True)
        )[::-1]
        return context
