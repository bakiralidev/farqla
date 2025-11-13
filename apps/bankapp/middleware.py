from django.utils import translation

class QueryParamLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get("lang")
        if lang in ["uz", "ru", "en"]:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        return self.get_response(request)