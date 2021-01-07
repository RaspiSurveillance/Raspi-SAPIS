#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2021 Denis Meyer
#
# This file is part of raspi-sapis
#

"""Server"""

import logging
import base64
import sys

from http import server
import ssl

from server.Handler import Handler
from tools.Helper import parse_args

class Server:

    def __init__(self, __prog__, settings):
        """Initialization

        :param settings: The settings
        """
        logging.info('Initializing')

        self.settings = settings

        self.keep_running = True

        # Parse command line arguments
        self.args = parse_args(__prog__, self.settings)
        self.running = False
        self.port = 8200

        # Initialize internally
        self._init()

    def _init(self):
        """Internal initialization"""
        logging.debug('Initializing')

        if ':' not in self.args.username_password:
            logging.error('Wrong format. Use "{}"'.format('username:password'))
            sys.exit()

        # Save given parameters
        self.settings.set('server', 'port', self.args.port)

        # Extract URL and port
        self.url = self.settings.get('server')['url']
        self.port = self.settings.get('server')['port']

        # Prepare the Handler
        Handler.USERNAME_PASSWORD_BASE64 = base64.b64encode(self.args.username_password.encode('utf-8'))
        Handler.settings = self.settings

    def _cleanup(self):
        """Cleans up all initialized resources"""
        logging.info('Cleaning up')
        self.running = False
        logging.info('Done cleaning up')

    def run(self):
        """Starts the main loop"""
        if self.running:
            logging.info('Already started')
            return

        if not self.running:
            self.running = True

        logging.info('Starting main loop')

        logging.info('Starting server at "{}:{}"'.format(self.url, self.port))
        address = (self.url, self.port)
        self.server = server.HTTPServer(address, Handler)
        if self.settings.get('server')['certfile'] and self.settings.get('server')['keyfile']:
            self.server.socket = ssl.wrap_socket(
                self.server.socket,
                certfile=self.settings.get('server')['certfile'],
                keyfile=self.settings.get('server')['keyfile'],
                server_side=True,
                ssl_version=ssl.PROTOCOL_TLS)
        # self.server.serve_forever()
        try:
            while (self.keep_running):
                try:
                    self.server.handle_request()
                except KeyboardInterrupt:
                    logging.info('Stopping server')
                    self.keep_running = False
        finally:
            logging.info('Stopped server')
            self._cleanup()
