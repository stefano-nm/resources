import json
import logging
import sys
from typing import Any

import cherrypy
import requests

from resources import Resources
from config import config

if __name__ == "__main__":
    cherrypy.tree.mount(Resources(**config, debug=True), "/", {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.engine.start()
    _, port = cherrypy.server.bound_addr
    endpoint = f"http://localhost:{port}"
    logging.basicConfig(level=logging.INFO)

    def get(method: str, **params: Any):
        query = f"{endpoint}/{method}"
        if len(params) > 0:
            query += "?" + "&".join([f"{name}={value}" for name, value in params.items()])
        response = requests.get(query)
        if response.status_code == 200:
            logging.info(method.upper() + ":" + json.dumps(response.json()))
        else:
            logging.info(method.upper() + ":" + str(response.status_code))


    get("resources")
    get("register", name="test", endpoint="test", token="test")
    get("resources")
    get("resource", name="test")
    get("unregister", name="test", token="wrong")
    get("resources")
    get("unregister", name="test", token="test")
    get("resources")

    sys.exit()
