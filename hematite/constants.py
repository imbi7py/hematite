# -*- coding: utf-8 -*-

from .compat.dictutils import OMD

CAP_MAP = None
ALL_HEADERS, REQUEST_HEADERS, RESPONSE_HEADERS = None, None, None


def _init_headers():
    # called (and del'd) at the very bottom
    global ALL_HEADERS, REQUEST_HEADERS, RESPONSE_HEADERS, CAP_MAP
    ALL_HEADERS = (GENERAL_HEADERS + REQUEST_ONLY_HEADERS
                   + RESPONSE_ONLY_HEADERS + ENTITY_HEADERS)
    REQUEST_HEADERS = GENERAL_HEADERS + REQUEST_ONLY_HEADERS + ENTITY_HEADERS
    RESPONSE_HEADERS = GENERAL_HEADERS + RESPONSE_ONLY_HEADERS + ENTITY_HEADERS
    CAP_MAP = dict([(h.lower(), h) for h in ALL_HEADERS])
    return


def http_header_case(text):
    # TODO: integrate into CAP_MAP default dict for caching?
    text = text.replace('_', '-').lower()
    try:
        return CAP_MAP[text]
    except KeyError:
        # Exceptions: ETag, TE, WWW-Authenticate, Content-MD5
        return '-'.join([p.capitalize() for p in text.split('-')])


GENERAL_HEADERS = ['Cache-Control',
                   'Connection',
                   'Date',
                   'Pragma',
                   'Trailer',
                   'Transfer-Encoding',
                   'Upgrade',
                   'Via',
                   'Warning']

REQUEST_ONLY_HEADERS = ['Accept',
                        'Accept-Charset',
                        'Accept-Encoding',
                        'Accept-Language',
                        'Authorization',
                        'Cookie',  # RFC6265
                        'Expect',
                        'From',
                        'Host',
                        'If-Match',
                        'If-Modified-Since',
                        'If-None-Match',
                        'If-Range',
                        'If-Unmodified-Since',
                        'Max-Forwards',
                        'Proxy-Authorization',
                        'Range',
                        'Referer',
                        'TE',
                        'User-Agent']

RESPONSE_ONLY_HEADERS = ['Accept-Ranges',
                         'Age',
                         'ETag',
                         'Location',
                         'Proxy-Authenticate',
                         'Retry-After',
                         'Server',
                         'Set-Cookie',  # RFC6265
                         'Vary',
                         'WWW-Authenticate']

ENTITY_HEADERS = ['Allow',
                  'Content-Encoding',
                  'Content-Language',
                  'Content-Length',
                  'Content-Location',
                  'Content-MD5',
                  'Content-Range',
                  'Content-Type',
                  'Expires',
                  'Last-Modified']

HOP_BY_HOP_HEADERS = ['Connection',
                      'Keep-Alive',
                      'Proxy-Authenticate',
                      'TE',
                      'Trailers',
                      'Transfer-Encoding',
                      'Upgrade']


_init_headers()
del _init_headers

CODE_REASONS = OMD({100: 'Continue',
                    101: 'Switching Protocols',
                    200: 'OK',
                    201: 'Created',
                    202: 'Accepted',
                    203: 'Non-Authoritative Information',
                    204: 'No Content',
                    205: 'Reset Content',
                    206: 'Partial Content',
                    300: 'Multiple Choices',
                    301: 'Moved Permanently',
                    302: 'Found',
                    303: 'See Other',
                    304: 'Not Modified',
                    305: 'Use Proxy',
                    307: 'Temporary Redirect',
                    400: 'Bad Request',
                    401: 'Unauthorized',
                    402: 'Payment Required',
                    403: 'Forbidden',
                    404: 'Not Found',
                    405: 'Method Not Allowed',
                    406: 'Not Acceptable',
                    407: 'Proxy Authentication Required',
                    408: 'Request Time-out',
                    409: 'Conflict',
                    410: 'Gone',
                    411: 'Length Required',
                    412: 'Precondition Failed',
                    413: 'Request Entity Too Large',
                    414: 'Request-URI Too Large',
                    415: 'Unsupported Media Type',
                    416: 'Requested range not satisfiable',
                    417: 'Expectation Failed',
                    500: 'Internal Server Error',
                    501: 'Not Implemented',
                    502: 'Bad Gateway',
                    503: 'Service Unavailable',
                    504: 'Gateway Time-out',
                    505: 'HTTP Version not supported'})
REASON_CODES = CODE_REASONS.inverted()