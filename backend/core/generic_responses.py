from typing import Any, Optional
from rest_framework.response import Response


def api_response(error: bool=False, data: Any=None, status_code: int=200, detail: Optional[str]=None, **extra):
    payload = {
        "error": error,
        "detail": detail,
        "data": data,
        "status_code": status_code,
    }
    if extra:
        payload.update(extra)
    return Response(payload, status=status_code)

def success_response(data: Any=None, detail: Optional[str]=None, status_code: int=200, **extra):
    return api_response(False, data, status_code, detail, **extra)

def error_response(detail: str, status_code: int=400, **extra):
    return api_response(True, None, status_code, detail, **extra)