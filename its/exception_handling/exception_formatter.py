from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.handler import ExceptionHandler
from drf_standardized_errors.types import ErrorResponse
import logging,traceback,sys
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from typing import Optional


class ExceptionRenderer(JSONRenderer):
    """
    Renders an exception
    """
    media_type = "application/problem+json"

class CustomExceptionHandler(ExceptionHandler):
    """
    Central custom ex eption handler for exceptions raised in whole code

    """
    def run(self) -> Optional[Response]:
        """entrypoint for handling an exception"""
        exc = self.convert_known_exceptions(self.exc)
        if self.should_not_handle(exc):
            return None
        exc = self.convert_unhandled_exceptions(exc)
        data = self.format_exception(exc)
        self.set_rollback()
        response = self.get_response(exc, data)
        self.context['request'].accepted_renderer = ExceptionRenderer() # Adding custom renderer class for exception handling
        self.report_exception(exc, response)
        return response

    def get_response(self, exc: exceptions.APIException, data: dict) -> Response:
        headers = self.get_headers(exc)
        return Response(data, status=exc.status_code, headers=headers)
   

class CustomExceptionFormatter(ExceptionFormatter):
    """
    Central exception formatter for exceptions raised in the whole 
    code.

    .. core::python

        {
            "type": error_response.type,
            # "code": error.code,
            "message": error.detail,
            "field_name": error.attr,
            "status_code": self.exc.status_code,
        }
    """
    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0]
        traceback.format_exc()
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        # logger.exception(f"Type -: {error_response.type} - Message: {error.detail} - Field: {error.attr} - Status: {self.exc.status_code} Filename :{filename} Line Number: {line_number} - Exception:{str(self.exc)}")
        return {
            "type": error_response.type,
            # "code": error.code,
            "message": error.detail,
            "field_name": error.attr,
            "status_code": self.exc.status_code,
        }