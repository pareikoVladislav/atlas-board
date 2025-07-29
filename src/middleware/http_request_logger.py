import logging
from time import monotonic

logger = logging.getLogger("http")

SENSITIVE_KEYS = [
    'login',
    'password',
    'token',
    'access_token',
    'auth',
    'secret'
]

def mask_sensetive_data(data):
    if not isinstance(data, dict):
        return data
    return {
        key: ('****' if key.lower() in SENSITIVE_KEYS else value)
        for key, value in data.items()
    }

class HttpRequestLoggerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = monotonic()

        response = self.get_response(request)

        duration = monotonic() - start_time
        method = request.method

        path = request.get_full_path()

        status = response.status_code
        try:
            query_params = mask_sensetive_data(request.GET.dict())
        except Exception:
            query_params = {}

        logger.info(f"{method} {path} {status} {duration:.3f}s | params: {query_params}")

        return response
