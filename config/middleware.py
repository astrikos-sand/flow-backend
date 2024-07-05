from django.http import HttpRequest, JsonResponse, HttpResponse

from apps.common.exceptions import HttpException, generic_http_exception


class HandleHttpExceptions:
    def __init__(self, get_response: callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_exception(self, _, exception: Exception) -> JsonResponse:
        print(exception, flush=True)
        if isinstance(exception, HttpException):
            return exception.to_json_response()
        else:
            return generic_http_exception.to_json_response()
