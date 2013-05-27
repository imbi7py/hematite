# -*- coding: utf-8 -*-

from operator import attrgetter

ALL, REQUEST, RESPONSE, CAP_MAP = None, None, None, None


def _init_headers():
    # called (and del'd) at the very bottom
    global ALL, REQUEST, RESPONSE, CAP_MAP
    ALL = GENERAL + REQUEST_ONLY + RESPONSE_ONLY + ENTITY
    REQUEST = GENERAL + REQUEST_ONLY + ENTITY
    RESPONSE = GENERAL + RESPONSE_ONLY + ENTITY
    CAP_MAP = dict([(h.lower(), h) for h in ALL])
    return


def http_header_case(text):
    try:
        return CAP_MAP[text.lower()]
    except KeyError:
        # Exceptions: ETag, TE, WWW-Authenticate, Content-MD5
        return '-'.join([p.capitalize() for p in text.split('-')])


def header2attr_name(text):
    return '_'.join(text.split('-')).lower()


def attr2header_name(text):
    return http_header_case(text.replace('_', '-'))


class HTTPHeaderField(object):
    def __init__(self, name, load=None, dump=None, encode=None,
                 read_only=False, doc=None):
        self.attr_name = header2attr_name(name)
        self.http_name = attr2header_name(name)
        self.stored_name = '_' + self.attr_name
        self.load = load
        self.dump = dump
        self.encode = encode
        self.getter = attrgetter('_' + name)  # TODO
        self.read_only = bool(read_only)
        self.doc = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        try:
            return self.getter(obj)
        except AttributeError:
            name = self.attr_name
            if name not in obj.known_headers:
                return None
            val = obj.known_headers[name]
            if self.load:
                val = self.load(val)
            setattr(obj, self.stored_name, val)
            return val

    def __set__(self, obj, value):
        if self.read_only:
            raise AttributeError("read-only field '%s'" % self.attr_name)
        setattr(obj, self.stored_name, value)

    def __delete__(self, obj):
        raise AttributeError("can't delete field '%s'" % self.attr_name)

    def __repr__(self):
        cn = self.__class__.__name__
        return '%s("%s", read_only=%r)' % (cn, self.attr_name, self.read_only)

    def encode(self, value, encoding='latin-1'):
        # TODO: hmm
        return self.http_name + ': ' + value.encode(encoding)


GENERAL = ['Cache-Control',
           'Connection',
           'Date',
           'Pragma',
           'Trailer',
           'Transfer-Encoding',
           'Upgrade',
           'Via',
           'Warning']

REQUEST_ONLY = ['Accept',
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

RESPONSE_ONLY = ['Accept-Ranges',
                 'Age',
                 'ETag',
                 'Location',
                 'Proxy-Authenticate',
                 'Retry-After',
                 'Server',
                 'Set-Cookie',  # RFC6265
                 'Vary',
                 'WWW-Authenticate']

ENTITY = ['Allow',
          'Content-Encoding',
          'Content-Language',
          'Content-Length',
          'Content-Location',
          'Content-MD5',
          'Content-Range',
          'Content-Type',
          'Expires',
          'Last-Modified']


_init_headers()
del _init_headers
