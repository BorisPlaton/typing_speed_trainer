from account.models import User


def get_users_list_by_statistics():
    queryset = (User.objects
                .select_related('statistics', 'profile')
                .order_by('-statistics__attempts_amount',
                          '-statistics__wpm',
                          '-statistics__accuracy'))
    return queryset
