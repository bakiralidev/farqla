# apps/bankapp/views_clicks.py
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from .models_clicks import URLClickStat, record_url_click

def go_redirect(request, model_name: str, pk: int, field_name: str):
    ct = get_object_or_404(ContentType, model=model_name)
    model_cls = ct.model_class()
    obj = get_object_or_404(model_cls, pk=pk)

    url = getattr(obj, field_name, None)
    if not url:
        raise Http404("URL field is empty or not found")

    # stat yozamiz
    record_url_click(obj, field_name, request, request.user if hasattr(request, "user") else None)
    return redirect(url)
