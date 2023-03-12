import time
from threading import Thread
from typing import List

import cherrypy

from .row import Row
from ..utils import Dispatcher, Supabase, post, delete


class CatalogBase(Dispatcher, Supabase):
    def __init__(
            self,
            supabase_endpoint: str,
            supabase_token: str,
            supabase_email: str,
            supabase_password: str,
            supabase_table: str,
            object_name: str = "Service",
            deletion_period: float = 60*60*24*7,
            debug: bool = False
    ):
        Supabase.__init__(
            self,
            endpoint=supabase_endpoint,
            public_token=supabase_token,
            email=supabase_email,
            password=supabase_password
        )
        Dispatcher.__init__(
            self,
            debug=debug
        )
        self._table = supabase_table
        self._object_name = object_name or "Service"
        self._deletion_period = deletion_period or 60*60*24*7

    def _select_new(self, items: List[Row]):
        now = time.time()
        new = []
        old = []
        for item in items:
            if item.timestamp + self._deletion_period < now:
                old.append(item)
            else:
                new.append(item)

        def _thread():
            for old_item in old:
                self.delete(self._table, old_item)

        Thread(target=_thread, daemon=True).start()
        return new

    def _catalog(self, **kwargs):
        catalog = self.select(self._table, row_type=Row)
        return [item.filter("name", "endpoint") for item in self._select_new(catalog)]

    def _object(self, name: str, **kwargs):
        objects = self.select(self._table, where={"name": name}, row_type=Row)
        objects = self._select_new(objects)
        if len(objects) == 0:
            raise cherrypy.HTTPError(404, f"{self._object_name} not found.")
        return objects[0].filter("name", "endpoint")

    @post
    def register(self, name: str, endpoint: str = None, token: str = None, **kwargs):
        objects = self.select(self._table, where={"name": str}, row_type=Row)
        objects = self._select_new(objects)
        if len(objects) == 0:
            self.insert(self._table, {
                "name": name,
                "endpoint": endpoint,
                "timestamp": time.time(),
                "token": token
            })
            return f"{self._object_name} registered."
        elif objects[0]["token"] == token:
            values = {"timestamp": time.time()}
            if endpoint is not None:
                values["endpoint"] = endpoint
            self.update(self._table, values, objects[0])
            return f"{self._object_name} updated."
        else:
            raise cherrypy.HTTPError("401", "Invalid token.")

    @delete
    def unregister(self, name: str, token: str = None, **kwargs):
        objects = self.select(self._table, where={"name": name}, row_type=Row)
        objects = self._select_new(objects)
        if len(objects) == 0:
            return f"{self._object_name} not registered."
        elif objects[0].token != token:
            raise cherrypy.HTTPError(401, "Invalid token.")
        else:
            self.delete(self._table, objects[0])
            return f"{self._object_name} unregistered."
