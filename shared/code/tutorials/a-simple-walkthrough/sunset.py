import os

import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import requests

cur_dir = os.path.abspath(os.path.dirname(__file__))
key_path = os.path.join(cur_dir, "key.pem")
cert_path = os.path.join(cur_dir, "cert.pem")


class Root:
    @cherrypy.expose
    def city(self, name):
        r = requests.post("https://localhost:8444/", timeout=(2, 2), json={
            "city": name
        }, verify=cert_path)

        if r.status_code != 200:
            raise cherrypy.HTTPError(500, r.text)

        cherrypy.response.headers["Content-Type"] = "text/plain"
        return "The sunset will occur at {} in {}".format(
            r.json()["sunset"], name
        )


def run():

    cherrypy.config.update({
        "environment": "production",
        "log.screen": True,
        "server.socket_port": 8443,
        "server.ssl_module": "builtin",
        "server.ssl_private_key": key_path,
        "server.ssl_certificate": cert_path
    })
    PIDFile(cherrypy.engine, 'sunset.pid').subscribe()
    cherrypy.quickstart(Root())


if __name__ == '__main__':
    run()
