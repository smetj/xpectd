#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#
#  Copyright 2022 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import falcon
import gunicorn
import argparse
import random
import gunicorn.app.base
import datetime
from time import sleep
from time import time
from croniter import croniter
from .tools import Config
from gevent import monkey

monkey.patch_all()


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="A webservice to simulate various outage scenarios.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--address",
        type=str,
        dest="address",
        default="127.0.0.1",
        help="The IP to bind to.",
    )
    parser.add_argument(
        "--port", type=int, dest="port", default=8080, help="The port to bind to."
    )
    parser.add_argument(
        "--workers",
        type=str,
        dest="workers",
        default=1,
        help="The number of processes to run.",
    )
    parser.add_argument(
        "--threads",
        type=str,
        dest="threads",
        default=10,
        help="The number of threads per process.",
    )
    parser.add_argument(
        "--plan",
        type=str,
        dest="plan",
        required=True,
        help="The plan file to load.",
    )

    return parser.parse_args()


class Server(gunicorn.app.base.BaseApplication):
    """
    The Gunicorn WSGI server    .

    Args:
        app: The WSGI app.
        options: The Gunicorn server options.
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.app = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.app


class Outage:
    """ """

    def __init__(
        self,
        outage_cron,
        outage_duration,
        outage_response,
        nominal_return_code,
        nominal_payload,
        nominal_min_duration,
        nominal_max_duration,
    ):
        self.outage_cron = outage_cron
        self.outage_duration = outage_duration
        self.outage_response = outage_response
        self.nominal_return_code = nominal_return_code
        self.nominal_payload = nominal_payload
        self.nominal_min_duration = nominal_min_duration
        self.nominal_max_duration = nominal_max_duration

        self.outage_enabled = False
        self.generate_responses = self.response_generator()

    def on_get(self, req, resp):
        if (
            self.outage_enabled
            or time()
            - croniter(self.outage_cron, datetime.datetime.utcnow()).get_prev()
            <= self.outage_duration
        ):
            response = next(self.generate_responses)
            sleep(random.uniform(response["min_duration"], response["max_duration"]))
            resp.body = response["payload"]
            resp.status = response["return_code"]
        else:
            sleep(random.uniform(self.nominal_min_duration, self.nominal_max_duration))
            resp.body = self.nominal_payload
            resp.status = self.nominal_return_code

    def response_generator(self):
        responses = []
        for entry in self.outage_response:
            responses += [entry for _ in range(entry["percentage"])]
        random.shuffle(responses)

        def generate_responses():
            while True:
                for response in responses:
                    yield response
                random.shuffle(responses)

        return generate_responses()

    def enable_outage(self):
        self.outage_enabled = True

    def disable_outage(self):
        self.outage_enabled = False


class ToggleOutage:
    def __init__(self, enable, disable):
        self.enable = enable
        self.disable = disable

    def on_post(self, req, resp, action):

        if action == "enable":
            self.enable()
            resp.media = {"status": "enabled"}
            resp.status = falcon.HTTP_200
        elif action == "disable":
            self.disable()
            resp.media = {"status": "disabled"}
            resp.status = falcon.HTTP_200


def main():

    args = parse_arguments()
    config = Config(args.plan).load()

    app = falcon.App(middleware=[])
    for plan in config.keys():

        outage = Outage(**config[plan])
        app.add_route(
            "/" + plan,
            outage,
        )
        app.add_route(
            "/" + plan + "/{action}",
            ToggleOutage(outage.enable_outage, outage.disable_outage),
        )

    Server(
        app,
        {
            "bind": f"{args.address}:{args.port}",
            "threads": args.threads,
            "workers": args.workers,
            "accesslog": "-",
            "disable_redirect_access_to_syslog": True,
            "worker_class": "gevent",
        },
    ).run()


if __name__ == "__main__":
    main()
