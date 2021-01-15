#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf8
#
# Copyright 2021 Denis Meyer
#
# This file is part of raspi-sapis
#

"""Helper"""

import os
import stat
import pwd
import grp
import sys
import logging
import argparse

TEMPLATE_FOLDER = 'templates'


def initialize_logger(settings):
    """Initializes the logger

    :param settings: The settings
    """
    if settings.log_to_file:
        basedir = os.path.dirname(settings.log_filename)

        if not os.path.exists(basedir):
            os.makedirs(basedir)

    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    logger.propagate = False

    logger.handlers = []

    handler_console = logging.StreamHandler(sys.stdout)
    handler_console.setLevel(settings.log_level)
    handler_console.setFormatter(logging.Formatter(
        fmt=settings.log_format, datefmt=settings.log_dateformat))
    logger.addHandler(handler_console)

    if settings.log_to_file:
        handler_file = logging.FileHandler(
            settings.log_filename, mode='w', encoding=None, delay=False)
        handler_file.setLevel(settings.log_level)
        handler_file.setFormatter(logging.Formatter(
            fmt=settings.log_format, datefmt=settings.log_dateformat))
        logger.addHandler(handler_file)


def get_ascii_art_banner():
    """Returns the ASCII-art banner

    :return: ASCII-art banner
    """
    return r"""
  _____                 _        _____         _____ _____  _____ 
 |  __ \               (_)      / ____|  /\   |  __ \_   _|/ ____|
 | |__) |__ _ ___ _ __  _ _____| (___   /  \  | |__) || | | (___  
 |  _  // _` / __| '_ \| |______\___ \ / /\ \ |  ___/ | |  \___ \ 
 | | \ \ (_| \__ \ |_) | |      ____) / ____ \| |    _| |_ ____) |
 |_|  \_\__,_|___/ .__/|_|     |_____/_/    \_\_|   |_____|_____/ 
                 | |                                              
                 |_| (C) 2021 Denis Meyer
"""


def parse_args(__prog__, settings):
    """Parses the command line arguments

    :param __prog__: Program name
    :param settings: The settings
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser(prog=__prog__)
    parser.add_argument('username_password', help='username:password')
    parser.add_argument('--port', required=False, type=int,
                        help='port number', default=settings.get('server')['port'])
    args = parser.parse_args()

    return args


def has_arguments(obj, arguments_list=[]):
    '''Checks whether the given object has all arguments in a given list

    :param obj: The object
    :param arguments_list: The list
    '''
    for arg in arguments_list:
        if not arg in obj:
            return False
    return True


def read_txt(filename):
    """Reads in a text file

    :param settings: The settings
    """

    outstr = ''

    with open(filename, 'r') as jf:
        outstr = jf.read()
    return outstr


def load_template(name, options={}):
    '''Loads a template and replaces options

    :param name: Name of the template
    :param options: Options to be replaced
    '''
    tmpl = read_txt('{}/{}.sh.tmpl'.format(TEMPLATE_FOLDER, name))
    for option in options:
        opt = ''
        if option.lower() == 'options':
            options_map = options[option]
            for o in options_map:
                opt = opt + ' ' + o + ' ' + str(options_map[o])
        else:
            opt = str(options[option])
        logging.debug('Replacing "{}" with "{}"'.format(option, opt))
        tmpl = tmpl.replace('${}'.format(option.upper()), opt)
    return tmpl


def create_script(_dir, script_folder, script_name, content):
    '''Creates folders, creates and writes the script, makes it executable'''
    logging.debug('Creating script')
    script_folder_path = '{}/{}'.format(_dir, script_folder)
    script_path = '{}/{}'.format(script_folder_path, script_name)

    logging.debug('Asserting folder')
    try:
        if not os.path.exists(script_folder_path):
            os.makedirs(script_folder_path)
    except Exception as e:
        logging.error('Failed to create folder "{}": {}'.format(script_folder_path, e))
        return False, script_folder_path, script_path

    logging.debug('Writing script')
    try:
        with open(script_path, 'w') as fwrite:
            fwrite.write(content)
    except Exception as e:
        logging.error('Failed to write template to "{}": {}'.format(script_path, e))
        return False, script_folder_path, script_path

    logging.debug('Making file executable and setting owner')
    try:
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)
        uid = pwd.getpwnam('pi').pw_uid
        gid = grp.getgrnam('pi').gr_gid
        os.chown(script_path, uid, gid)
    except Exception as e:
        logging.error('Failed to make file "{}" executable: {}'.format(script_path, e))
        return False, script_folder_path, script_path

    return True, script_folder_path, script_path
