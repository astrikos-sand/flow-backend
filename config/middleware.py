from django.http import HttpRequest, JsonResponse, HttpResponse
from django.core.exceptions import ValidationError

from rest_framework import status

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

        elif isinstance(exception, ValidationError):
            return HttpException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=exception.message_dict,
                ok=True,
            ).to_json_response()

        else:
            return generic_http_exception.to_json_response()


# TODO
from django.utils.deprecation import MiddlewareMixin


class DisableCsrfCheck(MiddlewareMixin):

    def process_request(self, req):
        attr = "_dont_enforce_csrf_checks"
        if not getattr(req, attr, False):
            setattr(req, attr, True)
