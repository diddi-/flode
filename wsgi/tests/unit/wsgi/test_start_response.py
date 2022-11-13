from unittest import TestCase

from wsgi.http_status import HttpStatus
from wsgi.testutil.start_response import StartResponse


class TestStartResponse(TestCase):
    def test_http_status_is_parsed_into_HttpStatus(self) -> None:
        start_response = StartResponse()

        start_response(HttpStatus.OK.to_wsgi_string(), [])
        self.assertEqual(HttpStatus.OK, start_response.http_response.status)

        start_response(HttpStatus.INTERNAL_SERVER_ERROR.to_wsgi_string(), [])
        self.assertEqual(HttpStatus.INTERNAL_SERVER_ERROR, start_response.http_response.status)
