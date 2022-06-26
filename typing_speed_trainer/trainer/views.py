from django.views.generic import TemplateView

from trainer.utils.mixins import TrainerResultMixin


class TypingTrainer(TemplateView, TrainerResultMixin):
    template_name = 'trainer/typing_trainer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.get_all_results_from_cache()
        return context
