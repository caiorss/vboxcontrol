#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""


from subprocess import PIPE, Popen
import platform
import os
import sys
import re
import zlib
from socket import socket
from socket import AF_INET, SOCK_STREAM, SHUT_RDWR
from socket import SOL_SOCKET, SO_REUSEADDR

localhost = '127.0.0.1'
allhosts = '0.0.0.0'

import logging
import logging.config

LOG_SETTINGS = {
    # --------- GENERAL OPTIONS ---------#
    'version': 1,
    'disable_existing_loggers': False,

        'root': {
            'level': 'NOTSET',
            'handlers': ['file'],
        },

    #---------- HANDLERS ---------------#
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'NOTSET',
            'formatter': 'detailed',
            'filename': 'client.log',
            'mode': 'a',
            'maxBytes': 10485760,
            'backupCount': 5,
        },
        'tcp' : {
            'class' : 'logging.handlers.SocketHandler',
            'level' :  'INFO',
            'host'  :  '192.168.1.2',
            'port'  :  9020,
            'formatter': 'detailed',
        },
    },

    # ----- FORMATTERS -----------------#
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(funcName)s() ' \
            '%(levelname)-8s %(message)s',
        },
        'verbose': {
        'format': '%(levelname)-8s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        'datefmt': '%a, %d %b %Y %H:%M:%S'

        },
        'email': {
            'format': 'Timestamp: %(asctime)s\nModule: %(module)s\n' \
            'Line: %(lineno)d\nMessage: %(message)s',
        },
    },
}

logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('root')


class Client(object):
    """
    Stream socket server class -- no definitive name
    """

    def __init__(self, host, port, buffersize=1024):


        self.host = host
        self.port = port
        self.buffersize = 1024


        # Clients IP's connected to this server
        self.clients = []
        # Client Sockets List
        self.connst = []

        self.sock = None

        self.mode = "shell"


    def connect(self):
        """
        Try only one time connect to server,
        if successfully connected returns True,
        False otherwise.
        """
        # create  socket handler
        s = socket(AF_INET, SOCK_STREAM)
        self.sock = s

        try:
            self.sock.connect((self.host, self.port))
            return True
        except:
            return False

    def connect_wait(self):
        """
        Keep Trying to connect to server, forever,
        even if server is down
        """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock = s

        logger.info("Client waiting server connection")

        while True:
            try:
                self.sock.connect((self.host, self.port))
                self.sendc("Client v%s Started from %s - %s " % ( VERSION, os.getcwd(), platform.platform() ))
                break
            except:
                pass
        logger.info("Client connected to server OK")


    def sendc(self, msg):
        """
        Send flow control message to client
        """
        self.sock.sendall(msg)

    def recevc(self):
        """
        Receive control message from client module
        """

        logger.info("wainting token")

        while True:
            data = self.sock.recv(self.buffersize)

            #print data
            if not data:
                continue
            else:
                # logger.debug("len(data) =%s" % len(data))
                # data2 = zlib.decompress(data)
                # logger.debug("len(data2) =%s" % len(data2))
                return data


    def handling_connections(self):
        pass

    def send(self):
        pass


class CommandClient(Client):

    def __init__(self, host, port, buffersize):
        super(CommandClient, self).__init__(host=host, port=port, buffersize=buffersize)


c = CommandClient(host='localhost', port=9090, buffersize=1024)
c.connect()
c.sendc("Hello world server")