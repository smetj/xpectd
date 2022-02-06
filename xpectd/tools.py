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
    "minProperties": 1,
    "patternProperties": {
        ".*": {
            "type": "object",
            "properties": {
                "outage_cron": {"type": "string"},
                "outage_duration": {"type": "number"},
                "outage_response": {
                    "type": "array",
                    "minItems": 1,
                    "contains": {
                        "type": "object",
                        "properties": {
                            "return_code": {"type": "number"},
                            "percentage": {"type": "number"},
                            "min_duration": {"type": "number"},
                            "max_duration": {"type": "number"},
                            "payload": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
                "nominal_return_code": {"type": "number"},
                "nominal_payload": {"type": "string"},
                "nominal_min_duration": {"type": "number"},
                "nominal_max_duration": {"type": "number"},
            },
            "additionalProperties": False,
        }
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

        for plan, content in config.items():
            total_spread = sum(
                [entry["percentage"] for entry in content["outage_response"]]
            )
            if total_spread != 100:
                raise Exception(
                    f"The total percentage of plan '{plan}' must be 100%. Currently at {total_spread}"
                )
