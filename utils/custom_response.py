import re
from rest_framework.status import is_client_error, is_success


class ResponseFormattingMiddleware:
    METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        path_info = request.META["PATH_INFO"]
        if path_info != '/swagger/' and path_info != '/redoc/':
            if request.method in self.METHOD:
                # response 형식
                response_format = {
                    'success': is_success(response.status_code),
                    'data': {},
                    'message': None
                }

                if hasattr(response, 'data') and getattr(response, 'data') is not None:
                    data = response.data
                    if is_client_error(response.status_code):
                        response_format['data'] = None
                        if "detail" in data:
                            response_format['message'] = data["detail"]
                        else:
                            response_format['message'] = data
                    else:
                        response_format['data'] = data
                        response_format['message'] = "success"

                    response.data = response_format
                    response.content = response.render().rendered_content
                else:
                    response.data = response_format

        return response