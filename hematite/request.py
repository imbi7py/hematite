# -*- coding: utf-8 -*-

from hematite.raw.request import RawRequest
from hematite.raw.envelope import (RequestEnvelope,
                                   RequestLine,
                                   Headers,
                                   HTTPVersion)

from hematite import serdes
from hematite.url import parse_hostinfo
from hematite.fields import REQUEST_FIELDS, HTTP_REQUEST_FIELDS

DEFAULT_METHOD = 'GET'
DEFAULT_VERSION = HTTPVersion(1, 1)
DEFAULT_SCHEME = 'http'
DEFAULT_PORT = 80

# headers, url, cookies

#_GENERIC_REQ_HEADERS = list(REQUEST)
#_GENERIC_REQ_HEADERS.remove('Host')


class Request(object):
    def __init__(self, method=None, url=None, **kw):
        self.method = method or DEFAULT_METHOD
        self.version = kw.pop('version', DEFAULT_VERSION)

        self._body = kw.pop('body', None)
        self._raw_url = url or None
        self._raw_headers = kw.pop('headers', Headers())

        self.url = self._raw_url
        self._init_headers()

        # TODO: maybe should defer this
        _url = self._url
        host_header = self.headers.get('Host')
        if not _url.host and host_header:
            if host_header:
                family, host, port = parse_hostinfo(host_header)
                _url.family, _url.host, _url.port = family, host, port
        if not host_header and _url.host:
            self.host = _url.http_request_host

    # TODO: could use a metaclass for this, could also build it at init
    _header_field_map = dict([(hf.http_name, hf)
                              for hf in HTTP_REQUEST_FIELDS])
    locals().update([(hf.attr_name, hf) for hf in REQUEST_FIELDS])
    _init_headers = serdes._init_headers
    _get_header_dict = serdes._get_headers

    @classmethod
    def from_raw_request(cls, raw_req):
        rl = raw_req.request_line
        kw = {'method': rl.method,
              'url': rl.url,
              'version': rl.version,
              'headers': raw_req.headers,
              'body': raw_req.body}
        return cls(**kw)

    def to_raw_request(self):
        req_line = RequestLine(self.method,
                               self._url.http_request_url,
                               self.version)
        headers = self._get_header_dict()
        return RawRequest(req_line, headers, self._body)

    # TODO: tmp
    def to_request_envelope(self):
        req_line = RequestLine(self.method,
                               self._url.http_request_url,
                               self.version)
        headers = self._get_header_dict()
        return RequestEnvelope(req_line, headers)

    @classmethod
    def from_bytes(cls, bytestr):
        rr = RawRequest.from_bytes(bytestr)
        return cls.from_raw_request(rr)

    def to_bytes(self):
        raw_req = self.to_raw_request()
        return raw_req.to_bytes()

    def validate(self):
        pass

    """
    def to_bytes(self):
        # TODO: field values are latin-1 or mime-encoded, but
        # are field names latin-1 or ASCII only?
        ret = [self.request_line]
        to_proc = set([h.lower() for h in self.headers])
        ret.append('Host: ' + self.url.http_request_host)
        to_proc.discard('host')
        for n, f in self.get_fields().items():
            v = getattr(self, f.attr_name)
            to_proc.discard(f.http_name.lower())
            if v:
                ret.append(f.http_name + ': ' + v)
        for h, v in self.headers.iteritems():
            if v and h.lower() in to_proc:
                ret.append(h + ': ' + v)
        ret.extend(['', ''])
        return '\r\n'.join(ret).encode('latin-1')

    @property
    def request_line(self):
        return ' '.join([self.method,
                         self.url.http_request_url,
                         'HTTP/%d.%d' % self.version])

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method=None):
        if method is None:
            method = DEFAULT_METHOD
        try:
            self._method = method.upper()
        except (AttributeError, TypeError):
            raise ValueError('http method expected string')

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if isinstance(url, URL):
            self._url = url  # TODO
        else:
            self._url = URL(url or '')
    """


"""
- method: methodcaller->upper, default GET
- http version: float() -> str
- path
- host
- user_agent
- accept
  - mime
  - charset
  - language

URL: scheme, netloc (host), path, params, query (, fragment?)
URL+: username, password, hostname, port

NB Blank headers are not sent
# TODO: incremental parsing/creation of Request
"""
