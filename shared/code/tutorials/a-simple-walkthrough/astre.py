from datetime import date, datetime
import os

from astral import Astral
import cherrypy
from cherrypy.process.plugins import Daemonizer, PIDFile
import pytz


class Root:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self) -> str:
        """
        Compute sunrise and sunset for the given city.
        """
        a = Astral()
        a.solar_depression = 'civil'

        params = cherrypy.request.json
        city_name = params["city"] or ""
        try:
            city = a[city_name]
        except KeyError:
            return {"error": "unknown city"}

        tz = pytz.timezone(city.timezone)

        sun = city.sun(date=date.today(), local=False)
        result = {}
        for k, v in sun.items():
            if isinstance(v, datetime):
                result[k] = v.astimezone(tz).isoformat()
            else:
                result[k] = v
        return result


def run():
    cur_dir = os.path.abspath(os.path.dirname(__file__))

    cherrypy.config.update({
        "environment": "production",
        "log.screen": True,
        "server.socket_port": 8444,
        "server.ssl_module": "builtin",
        "server.ssl_private_key": os.path.join(cur_dir, "key.pem"),
        "server.ssl_certificate": os.path.join(cur_dir, "cert.pem")
    })
    PIDFile(cherrypy.engine, 'astre.pid').subscribe()
    cherrypy.quickstart(Root())


if __name__ == '__main__':
    run()
