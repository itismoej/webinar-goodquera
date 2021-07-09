from django.http import Http404

from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404 as _get_object_or_404


def get_object_or_404(klass, *args, **kwargs):
    try:
        return _get_object_or_404(klass, *args, **kwargs)
    except Http404:
        raise NotFound('404 not found')
