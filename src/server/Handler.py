#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2021 Denis Meyer
#
# This file is part of raspi-sapis
#

"""Streaming handler"""

import logging
import subprocess
from http import server
import json
import os
import requests

from tools.Helper import has_arguments, load_template, create_script


class Handler(server.BaseHTTPRequestHandler):
    USERNAME_PASSWORD_BASE64 = ''
    settings = {}
    FOLDER_SCRIPTS_GENERATED = 'scripts_generated'

    def _do_authhead(self):
        '''Does the authentication'''
        logging.debug('Send authentication header')

        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm=\"Please enter your username and password\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_OK(self):
        '''Writes OK to out'''
        content = 'OK'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def _send_NOT_OK(self):
        '''Writes NOT OK to out'''
        content = 'NOT OK'
        self.send_response(400)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def _execute_start_camerastream(self, body):
        '''Executes start camerastream script'''
        logging.debug('Executing start camerastream script')

        logging.debug('Loading JSON body')
        json_body = {}
        logging.info(body)
        try:
            json_body = json.loads(body)
            logging.info(json_body)
        except Exception as e:
            logging.error('Failed to load JSON body: {}'.format(e))
            return False

        logging.debug('Checking arguments')
        if not has_arguments(json_body, ['name', 'password']):
            return False

        _dir = self.settings.get('camerastream')['dir']

        logging.debug('Loading template')
        template_name = 'start_camerastream'
        script_name = '{}.sh'.format(template_name)
        tmpl = ''
        try:
            tmpl = load_template(template_name, {
                'dir': _dir,
                'name': json_body['name'],
                'password': json_body['password'],
                'options': json_body['options'] if has_arguments(json_body, ['options']) else {}
            })
        except Exception as e:
            logging.error(
                'Failed to load template "{}": {}'.format(script_name, e))
            return False

        create_script_result = create_script(
            _dir, self.FOLDER_SCRIPTS_GENERATED, script_name, tmpl)
        if not create_script_result[0]:
            return False
        script_folder_path = create_script_result[1]

        cmd = 'cd {} ; ./{} ;'.format(script_folder_path, script_name)

        logging.debug('Executing command {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        '''
        (output, err) = p.communicate()
        logging.debug('>>> Command output: {}'.format(output))
        logging.debug('>>> Command exit status/return code: {}'.format(p_status))
        '''

        return p_status == 0

    def _execute_start_surveillance(self, body):
        '''Executes start surveillance script'''
        logging.debug('Executing start surveillance script')

        logging.debug('Loading JSON body')
        json_body = {}
        logging.info(body)
        try:
            json_body = json.loads(body)
            logging.info(json_body)
        except Exception as e:
            logging.error('Failed to load JSON body: {}'.format(e))
            return False

        _dir = self.settings.get('surveillance')['dir']

        logging.debug('Loading template')
        template_name = 'start_surveillance'
        script_name = '{}.sh'.format(template_name)
        tmpl = ''
        try:
            tmpl = load_template(template_name, {
                'dir': _dir,
                'options': json_body['options'] if has_arguments(json_body, ['options']) else {}
            })
        except Exception as e:
            logging.error(
                'Failed to load template "{}": {}'.format(script_name, e))
            return False

        create_script_result = create_script(
            _dir, self.FOLDER_SCRIPTS_GENERATED, script_name, tmpl)
        if not create_script_result[0]:
            return False
        script_folder_path = create_script_result[1]

        cmd = 'cd {} ; ./{} ;'.format(script_folder_path, script_name)

        logging.debug('Executing command {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        '''
        (output, err) = p.communicate()
        logging.debug('>>> Command output: {}'.format(output))
        logging.debug('>>> Command exit status/return code: {}'.format(p_status))
        '''

        return p_status == 0

    def _execute_startup(self, body):
        '''Executes startup script'''
        logging.debug('Executing startup script')

        logging.debug('Loading JSON body')
        json_body = {}
        try:
            json_body = json.loads(body)
            logging.info(json_body)
        except Exception as e:
            logging.error('Failed to load JSON body: {}'.format(e))
            return False

        logging.debug('Checking arguments')
        if not has_arguments(json_body, ['id']):
            return False

        server_id = json_body['id']
        if not server_id in self.settings.get('servers'):
            logging.info('Server ID "{}" not configured'.format(server_id))
            return False

        server_url = self.settings.get('servers')[server_id]['power_on']
        logging.info('Server URL for starting up server ID "{}": {}'.format(server_id, server_url))

        response = requests.put(server_url, data={})

        return response.status_code >= 200 and response.status_code< 300

    def _execute_shutdownMaster(self, body):
        '''Executes startup script'''
        logging.debug('Executing startup master script')

        logging.debug('Loading JSON body')
        json_body = {}
        try:
            json_body = json.loads(body)
            logging.info(json_body)
        except Exception as e:
            logging.error('Failed to load JSON body: {}'.format(e))
            return False

        logging.debug('Checking arguments')
        if not has_arguments(json_body, ['id']):
            return False

        server_id = json_body['id']
        if not server_id in self.settings.get('servers'):
            logging.info('Server ID "{}" not configured'.format(server_id))
            return False

        server_url = self.settings.get('servers')[server_id]['power_off']
        logging.info('Server URL for shutting down server ID "{}": {}'.format(server_id, server_url))

        response = requests.put(server_url, data={})

        return response.status_code >= 200 and response.status_code < 300

    def _execute_stop_camerastream(self):
        '''Executes stop camerastream script'''
        logging.debug('Executing stop camerastream script')

        _dir = self.settings.get('camerastream')['dir']

        logging.debug('Loading template')
        template_name = 'stop_camerastream'
        script_name = '{}.sh'.format(template_name)
        tmpl = ''
        try:
            tmpl = load_template(template_name, {})
        except Exception as e:
            logging.error(
                'Failed to load template "{}": {}'.format(script_name, e))
            return False

        create_script_result = create_script(
            _dir, self.FOLDER_SCRIPTS_GENERATED, script_name, tmpl)
        if not create_script_result[0]:
            return False
        script_folder_path = create_script_result[1]

        cmd = 'cd {} ; ./{} ;'.format(script_folder_path, script_name)

        logging.debug('Executing command {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        '''
        (output, err) = p.communicate()
        logging.debug('>>> Command output: {}'.format(output))
        logging.debug('>>> Command exit status/return code: {}'.format(p_status))
        '''

        return p_status == 0

    def _execute_stop_surveillance(self):
        '''Executes stop surveillance script'''
        logging.debug('Executing stop surveillance script')

        _dir = self.settings.get('surveillance')['dir']

        logging.debug('Loading template')
        template_name = 'stop_surveillance'
        script_name = '{}.sh'.format(template_name)
        tmpl = ''
        try:
            tmpl = load_template(template_name, {})
        except Exception as e:
            logging.error(
                'Failed to load template "{}": {}'.format(script_name, e))
            return False

        create_script_result = create_script(
            _dir, self.FOLDER_SCRIPTS_GENERATED, script_name, tmpl)
        if not create_script_result[0]:
            return False
        script_folder_path = create_script_result[1]

        cmd = 'cd {} ; ./{} ;'.format(script_folder_path, script_name)

        logging.debug('Executing command {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        '''
        (output, err) = p.communicate()
        logging.debug('>>> Command output: {}'.format(output))
        logging.debug('>>> Command exit status/return code: {}'.format(p_status))
        '''

        return p_status == 0

    def _execute_shutdown(self):
        '''Executes shutdown script'''
        logging.debug('Executing shutdown script')

        _dir = self.settings.get('shutdown')['dir']

        logging.debug('Loading template')
        template_name = 'shutdown'
        script_name = '{}.sh'.format(template_name)
        tmpl = ''
        try:
            tmpl = load_template(template_name, {})
        except Exception as e:
            logging.error(
                'Failed to load template "{}": {}'.format(script_name, e))
            return False

        create_script_result = create_script(
            _dir, self.FOLDER_SCRIPTS_GENERATED, script_name, tmpl)
        if not create_script_result[0]:
            return False
        script_folder_path = create_script_result[1]

        cmd = 'cd {} ; ./{} ;'.format(script_folder_path, script_name)

        logging.debug('Executing command {}'.format(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()

        '''
        (output, err) = p.communicate()
        logging.debug('>>> Command output: {}'.format(output))
        logging.debug('>>> Command exit status/return code: {}'.format(p_status))
        '''

        return p_status == 0

    def do_HEAD(self):
        '''HEAD method'''
        logging.debug('Handling HEAD')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        '''GET method'''
        logging.debug('Handling GET')

        header_auth = self.headers.get('Authorization')
        if header_auth is None:
            logging.debug('Not authorized - no auth header set')
            self._do_authhead()
            self.wfile.write(b'no auth header received')
        elif header_auth == 'Basic ' + self.USERNAME_PASSWORD_BASE64.decode('UTF-8'):
            logging.debug('Authorized')
            self._send_OK()

    def do_PUT(self):
        '''PUT method'''
        logging.debug('Handling PUT')

        header_auth = self.headers.get('Authorization')
        if header_auth is None:
            logging.debug('Not authorized - no auth header set')
            self._do_authhead()
            self.wfile.write(b'no auth header received')
        elif header_auth == 'Basic ' + self.USERNAME_PASSWORD_BASE64.decode('UTF-8'):
            logging.debug('Authorized')

            try:
                if not self.settings.get('api')[self.path]:
                    logging.info('API endpoint not activated')
                    self._send_NOT_OK()
                    return
            except:
                self.send_error(404)
                self.end_headers()
                return

            if self.path == '/start/camerastream':
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                if self._execute_start_camerastream(body.decode()):
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            elif self.path == '/start/surveillance':
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                if self._execute_start_surveillance(body.decode()):
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            elif self.path == '/stop':
                if self._execute_stop_camerastream() and self._execute_stop_surveillance():
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            elif self.path == '/shutdown':
                self._execute_stop_camerastream()
                self._execute_stop_surveillance()
                if self._execute_shutdown():
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            elif self.path == '/startup':
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                if self._execute_startup(body):
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            elif self.path == '/shutdown/master':
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                if self._execute_shutdownMaster(body.decode()):
                    self._send_OK()
                else:
                    self._send_NOT_OK()
            else:
                self.send_error(404)
                self.end_headers()
