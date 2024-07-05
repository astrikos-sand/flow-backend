from django.http import JsonResponse
from rest_framework import status


class HttpException(Exception):
    def __init__(self, message: str, status_code: int, ok: bool):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.ok = ok

    def __str__(self):
        return f"HttpException({self.status_code}): {self.message}"

    def to_json_response(self) -> JsonResponse:
        return JsonResponse(
            {
                "message": self.message,
                "ok": self.ok,
            },
            status=self.status_code,
        )


bad_request = HttpException(
    status_code=status.HTTP_400_BAD_REQUEST,
    message="Bad request",
    ok=True,
)

does_not_exist = HttpException(
    status_code=status.HTTP_404_NOT_FOUND,
    message="Does not exist",
    ok=True,
)

form_filled_incorrectly = HttpException(
    status_code=status.HTTP_400_BAD_REQUEST,
    message="Form filled incorrectly",
    ok=True,
)

generic_http_exception = HttpException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    message="Internal Server Error",
    ok=False,
)
