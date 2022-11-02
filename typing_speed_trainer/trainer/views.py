from django.views.generic import TemplateView

from trainer.services import get_last_cached_results_with_users, sort_results_by_time


class TypingTrainer(TemplateView):
    """The main page with the typing trainer."""

    template_name = 'trainer/typing_trainer.html'

    def get_context_data(self, **kwargs):
        """
        Populates a context with last cached typing results and
        their users.
        """
        context = super().get_context_data(**kwargs)
        context.update({'other_users_results': sort_results_by_time(get_last_cached_results_with_users(10))})
        return context
