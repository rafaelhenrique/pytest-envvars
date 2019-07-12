from django.conf import settings
from django.views.generic import ListView

from tests.pytest_envvars_django_test.core.models import Product

GLOBAL_VARIABLE = settings.PYTEST_ENVVAR_GENERIC_USE


class ProductList(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['pytest_envvar_bool'] = settings.PYTEST_ENVVAR_BOOL
        context['pytest_envvar_str'] = settings.PYTEST_ENVVAR_STR
        context['pytest_envvar_int'] = settings.PYTEST_ENVVAR_INT
        context['pytest_envvar_float'] = settings.PYTEST_ENVVAR_FLOAT
        context['pytest_envvar_list'] = settings.PYTEST_ENVVAR_LIST
        context['pytest_envvar_tuple'] = settings.PYTEST_ENVVAR_TUPLE
        context['pytest_envvar_generic_use'] = GLOBAL_VARIABLE
        return context
