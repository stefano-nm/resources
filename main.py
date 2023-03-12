import cherrypy

from config import config
from resources import Resources


def create_app():
    app = cherrypy.tree.mount(Resources(**config), "/", {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.config.update({'engine.autoreload.on': False})
    cherrypy.server.unsubscribe()
    cherrypy.engine.start()
    return app
