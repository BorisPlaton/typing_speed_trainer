from django.views.generic import ListView
from django.views.generic.detail import DetailView
from sorl.thumbnail import delete
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from account.forms import ChangeProfilePhotoForm, ChangeProfileSettingsForm
from account.mixins import ElidedPaginationMixin
from account.models import Profile
from account.selectors import get_users_list_by_statistics
from type_results.services import get_all_user_results


class UsersList(ElidedPaginationMixin, ListView):
    """The page with all users of site."""

    template_name = 'account/users_list.html'
    context_object_name = 'users'
    queryset = get_users_list_by_statistics()
    paginate_by = 50

    pagination_on_ends = 1
    pagination_on_each_side = 2
    paginator_ellipsis = '...'


class Account(DetailView):
    """The user profile page."""

    model = Profile
    context_object_name = 'user_profile'
    template_name = 'account/profile.html'

    forms = {
        'load_photo_form': ChangeProfilePhotoForm,
        'user_settings_form': ChangeProfileSettingsForm,
    }
    forms_on_models = {
        'delete_photo_form': Profile,
    }
    forms_on_models_fields = {
        'delete_photo_form': ['photo'],
    }

    def get_context_data(self, **kwargs):
        """
        Populates a context with last user's results and if he has
        a default profile picture.
        """
        context = super().get_context_data(**kwargs)
        context['results'] = get_all_user_results(self.kwargs['pk'])
        context['has_default_photo'] = self.object._meta.get_field('photo').default == self.object.photo
        return context

    def get_object(self, queryset=None):
        """
        Joins a `Statistic` and a `User` model.
        """
        queryset = (self.model.objects
                    .select_related('user')
                    .select_related('user__statistics'))
        return super().get_object(queryset)


@method_decorator(login_required, name='dispatch')
class UpdateProfileSettings(UpdateView):
    """The view-class for the profile settings of user."""

    model = Profile
    fields = ['is_email_shown', 'are_results_shown']

    def get_object(self, queryset=None):
        return self.request.user_id.profile


@method_decorator(login_required, name='dispatch')
class UpdateProfilePhoto(UpdateView):
    """Process uploading a user photo."""

    model = Profile
    fields = ['photo']

    def get_object(self, queryset=None):
        return self.request.user_id.profile


@method_decorator(login_required, name='dispatch')
class DeleteProfilePhoto(UpdateView):
    """The view-class for a user photo deletion."""

    model = Profile
    fields = ['photo']

    def get_object(self, queryset=None):
        return self.request.user_id.profile

    def form_valid(self, form):
        default_photo = self.object._meta.get_field('photo').default
        if self.object.photo != default_photo:
            delete(self.object.photo)
            self.object.photo = default_photo
            self.object.save()
        return super().form_valid(form)
