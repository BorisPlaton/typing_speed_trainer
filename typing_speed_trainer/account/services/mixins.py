from django.core.paginator import Paginator


class ElidedPaginationMixin:
    pagination_on_each_side = 2
    pagination_on_ends = 2
    paginator_ellipsis = '...'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if paginator := context.get('paginator'):
            paginator: Paginator
            paginator.ELLIPSIS = self.paginator_ellipsis
            context['page_range'] = paginator.get_elided_page_range(
                number=context.get('page_obj').number,
                on_each_side=self.pagination_on_each_side,
                on_ends=self.pagination_on_ends,
            )
        return context
