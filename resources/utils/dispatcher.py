import json
from enum import Enum
from typing import Dict, Callable, Tuple

import cherrypy
import markdown2

_type_field_name = "__type__"


class _MethodType(Enum):
    GET = 0
    POST = 1
    DELETE = 2
    PUT = 3


def _method_decorator(method_type: _MethodType):
    def decorator(method: Callable):
        setattr(method, _type_field_name, method_type)
        return method

    return decorator


get = _method_decorator(_MethodType.GET)
post = _method_decorator(_MethodType.POST)
delete = _method_decorator(_MethodType.DELETE)
put = _method_decorator(_MethodType.PUT)


class Dispatcher:
    exposed = True

    def __init__(self, debug: bool = False):
        self._debug = debug
        self._methods: Dict[str, Tuple[_MethodType, Callable]] = {}
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, _type_field_name):
                method_type = getattr(method, _type_field_name)
                self._methods[name] = (method_type, method)

    def POST(self, *uri, **params):
        return self._parse_request(_MethodType.POST, uri, params)

    def GET(self, *uri, **params):
        return self._parse_request(_MethodType.GET, uri, params)

    def DELETE(self, *uri, **params):
        return self._parse_request(_MethodType.DELETE, uri, params)

    def PUT(self, *uri, **params):
        return self._parse_request(_MethodType.PUT, uri, params)

    def _parse_request(self, method_type: _MethodType, uri: tuple, params: dict):
        if len(uri) == 0:
            return markdown2.markdown_path("README.md")
        if len(uri) != 1:
            raise cherrypy.HTTPError(
                400, "Bad Request. Path must contain only the method name."
            )
        method_name = uri[0]
        if method_name not in self._methods:
            raise cherrypy.HTTPError(
                404, "Bad Request. Method doesn't exist."
            )
        real_type, method = self._methods[method_name]
        if not self._debug and method_type != real_type:
            raise cherrypy.HTTPError(400, "Bad Request. Incorrect method.")
        try:
            response = method(**params)
            return json.dumps(response)
        except cherrypy.HTTPError:
            raise
        except BaseException:
            raise cherrypy.HTTPError(500)
