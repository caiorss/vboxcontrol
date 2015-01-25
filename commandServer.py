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
allhosts  = '0.0.0.0'


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
            'filename': 'server.log',
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



class Server(object):
    """
    Stream socket server class -- no definitive name
    """

    def __init__(self, host, port, maxconn=10, buffersize=1024):



        self.host = host
        self.port = port
        self.maxconn = maxconn
        self.buffersize = buffersize

        # Clients IP's connected to this server
        self.clients = []
        # Client Sockets List
        self.conns  = []

        # In the beggining accept only one client
        # @TODO: Handle multiple clients
        self.addr = ""
        self.conn = None

        # create  socket handler
        s = socket(AF_INET, SOCK_STREAM)
        # Reuse address
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((host, port))

        s.listen(maxconn)
        self.sock = s

    def __str__(self):
        txt = "addr %s" % str(self.addr)
        txt += "\n%s" % str(self.conns)
        return txt

    def connect(self):
        """
        Accept connection from client
        """
        print "Waiting Clients"

        logger.debug("Waiting client connection")
        conn, addr = self.sock.accept()
        self.clients.append(addr)
        self.conns.append(conn)
        self.conn = conn
        self.addr = addr


        client = self.recevc()
        logger.debug("%s", {'conn':conn, 'addr':addr, 'client': client})

        print "Received connection from", addr[0]
        print client

    def sendc(self, msg):
        """
        Send flow control message to client
        """
        self.conn.sendall(msg)

    def recevc(self):
        """
        Receive control message from client module
        """
        conn = self.conn

        while True:
            data = conn.recv(self.buffersize)

            #print data
            if not data:
                raise Exception("Error connection closed")
            else:
                #logger.debug("len(data) =%s" % len(data))
                #data2 = zlib.decompress(data)
                #logger.debug("len(data2) =%s" % len(data2))
                return data

    def getclients(self):
        logger.debug("Waiting client connection")
        self.sock.settimeout(None)

        for i in range(8):
            logger.info("i = %s" % i)
            try:
                logger.debug("accepting connection")
                conn, addr = self.sock.accept()
                logger.debug("connection accepted")
                self.clients.append(addr[0])  # Clients hostnames or ip's
                self.conns.append(conn)       # Clients sockets
                self.conn.settimeout(0.1)
                self.conn = conn


                client = self.recevc()

                print "Get client from %s  - %s" % (addr[0], client)
            except:
                pass

        logger.info("%s" % {'clients': self.clients, 'conn': self.conn, 'addr': self.addr } )
        self.sock.settimeout(None)


    def handling_connections(self):
        pass

    def send(self):
        pass

class CommandServer(Server):

    def __init__(self, host='0.0.0.0', port=9090, buffersize=1024):
        super(CommandServer, self).__init__(host=host, port=port, buffersize=buffersize)

        self.getclients()


s = CommandServer('0.0.0.0', 9090, buffersize=1024)
print s.recevc()



