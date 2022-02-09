#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tools.py
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

import yaml
from jsonschema import validate

SCHEMA = {
    "type": "object",
    "properties": {
        "scenarios": {
            "type": "array",
            "minItems": 1,
            "contains": {
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string"},
                    "response": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "number"},
                            "payload": {"type": "string"},
                            "min_time": {"type": "number"},
                            "max_time": {"type": "number"},
                        },
                        "additionalProperties": False,
                    },
                    "outage": {
                        "type": "object",
                        "properties": {
                            "schedule": {"type": "string"},
                            "duration": {"type": "number"},
                            "response": {
                                "type": "array",
                                "minItems": 1,
                                "contains": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "number"},
                                        "percentage": {"type": "number"},
                                        "payload": {"type": "string"},
                                        "min_time": {"type": "number"},
                                        "max_time": {"type": "number"},
                                    },
                                    "additionalProperties": False,
                                },
                            },
                        },
                    },
                },
            },
        },
        "additionalProperties": False,
    },
}


class Config:
    def __init__(self, filename):

        self.filename = filename
        self.config = self.load()

    def load(self):

        with open(self.filename) as config:
            content = yaml.safe_load(config)
            validate(content, SCHEMA)
            self.validation(content)
            return content

    def validation(self, config):

        for scenario in config["scenarios"]:
            total_spread = sum(
                [entry["percentage"] for entry in scenario["outage"]["response"]]
            )
            if total_spread != 100:
                raise Exception(
                    f"The total percentage of plan '{scenario['endpoint']}' must be 100%. Currently at {total_spread}"
                )
