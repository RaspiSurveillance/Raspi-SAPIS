#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2021 Denis Meyer
#
# This file is part of raspi-sapis
#

__prog__ = 'RaspiSAPIS'
__version__ = '1.0'

"""
Main

Usage: "python raspi-sapis.py <username>:<password> [--port 8200]"
"""

import logging

from tools.Helper import initialize_logger, get_ascii_art_banner
from tools.Settings import Settings
from server.Server import Server

if __name__ == "__main__":
    settings = Settings()
    initialize_logger(settings)

    logging.info(get_ascii_art_banner())

    server = Server(__prog__, settings)
    server.run()
