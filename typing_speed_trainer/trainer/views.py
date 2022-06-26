from django.http import JsonResponse
from django.views.generic import TemplateView

from trainer.utils.mixins import TrainerResultMixin
from trainer.utils.shortcuts import get_correct_template_path


class TypingTrainer(TemplateView):
    template_name = 'trainer/typing_trainer.html'


class ResultsList(TrainerResultMixin):

    def get(self, request):
        data = self.get_result_templates()
        data.update({
            'resultsData': self.get_all_results_from_cache(),
        })
        return JsonResponse(data)

    @staticmethod
    def get_result_templates() -> dict:
        with (
            open(get_correct_template_path(
                'trainer', 'includes', 'results_list.html'
            )) as list_template_file,
            open(get_correct_template_path(
                'trainer', 'includes', 'last_result.html'
            )) as res_template_file,
        ):
            results_list_template = list_template_file.read()
            result_template = res_template_file.read()
        return {
            'resultsListTemplate': results_list_template,
            'resultTemplate': result_template,
        }
