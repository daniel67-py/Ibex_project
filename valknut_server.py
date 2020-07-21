#!/usr/bin/python3
#-*- coding: Utf-8 -*-
import re
import os
import sys
import csv
import sqlite3
from jinja2 import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from wsgiref.simple_server import make_server

from valknut_gss import *

####################################################################################################
### Valknut - Micro Server, GSS & SQLite3 manager
### developped by Meyer Daniel for Python 3, July 2020
### this is version 0.1.0
####################################################################################################

####################################################################################################
### Valknut_Server class
####################################################################################################
class Valknut_Server():
    ### initialization of the server, debuging is False and socket port is 8008 ###
    def __init__(self, debuging = False, port = 8008):
        self.debuging = debuging
        self.port = port
        self.environ = ''
        self.contain = []
        self.deserve = []

    ### transmission function is here to fill the deserve variable ###
    def transmission(self, **from_gss):
        self.deserve.append({
            "path": from_gss.get('path'),
            "contains": from_gss.get('contains'),
            })
        self.contain.append(from_gss.get('path'))

    ### container_check is here to get the filenames into the container folder ###
    def container_check(self):
        ### formating for the filenames, adding '/' in front of them ###
        adding = os.listdir('container')
        for x in range(0, len(adding)):
            adding[x] = "/" + adding[x]
        
        self.contain += adding
                                  
    ### this is the application of the server ###
    ### it deserve the files of the container folder ###
    ### and deserve the pages defined by the user in his program ###
    def app(self, environ, start_response):
        ### first, take the 'environ' variables ###
        self.environ = environ

        ### then, if you want a 'debuging' environment ###
        if self.debuging == True:
            self.debug_environment()
               
        ### if the request is defined by user in his program ###
        for x in range(0, len(self.deserve)):
            if environ['PATH_INFO'] == self.deserve[x]["path"]:
                status = '200 OK'
                headers = [('Content-type', 'text/html; charset=utf-8')]
                start_response(status, headers)
                ret = [self.deserve[x]["contains"].encode("utf-8")]
                return ret
            
        ### if the request is the root of the server ###
        if environ['PATH_INFO'] == '/':
            status = '200 OK'
            headers = [('Content-type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            main_page = Valknut_gss()
            main_page.file = "templates/index.md"
            main_page.use_template = "templates/index.html"
            main_page.project_title = "Valknut Index Page"
            main_page.project_header = "Valknut Root Index Page"
            main_page.project_footer = "Valknut is under licence - July 2020 - Daniel Meyer"
            main_page.project_index = self.contain
            main_page.feedback = 1
            gss_ret = main_page.generate()
            ret = [gss_ret.encode("utf-8")]
            return ret
        
        ### if the request is some of the formated filenames ###
        elif environ['PATH_INFO'] in self.contain and environ['REQUEST_METHOD'] == "GET":
            status = '200 OK'
            headers = [('Content-type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            ### generate the static page with Valknut_gss class ###
            static_page = Valknut_gss()
            static_page.file = f"container/{environ['PATH_INFO']}"
            static_page.project_title = environ['PATH_INFO']
            static_page.project_header = environ['PATH_INFO']
            static_page.project_footer = "this program is under licence - July 2020 - Daniel Meyer"
            static_page.feedback = 1
            gss_ret = static_page.generate()
            ### return the result ###            
            ret = [gss_ret.encode("utf-8")]
            return ret
        
        ### in case of mistake, return an error page ###
        else:
            status = '200 OK'
            headers = [('Content-type', 'text/plain; charset=utf-8')]
            start_response(status, headers)
            ret = ["No No Nooo... You didn't say the magic world ! Get back or give me a valid url...".encode("utf-8")]
            return ret

    ### the 'debuging' function, will return the 'environ' variables in the python's shell ###
    def debug_environment(self):
        print(''.zfill(100))
        print('0' + 'VALKNUT MICRO SERVER DEBUG ENVIRONMENT VARIABLES RETURNS'.center(98) + '0')
        print(''.zfill(100))
        print('  path info         : ' + self.environ['PATH_INFO'])
        print('  request method    : ' + self.environ['REQUEST_METHOD'])
        print('  script name       : ' + self.environ['SCRIPT_NAME'])
        print('  query string      : ' + self.environ['QUERY_STRING'])
        print('  content type      : ' + self.environ['CONTENT_TYPE'])
        print('  content length    : ' + self.environ['CONTENT_LENGTH'])
        print('  server name       : ' + self.environ['SERVER_NAME'])
        print('  server port       : ' + self.environ['SERVER_PORT'])
        print('  server protocol   : ' + self.environ['SERVER_PROTOCOL'])
        print('  wsgi.version      : ' + str(self.environ['wsgi.version']))
        print('  wsgi.input        : ' + str(self.environ['wsgi.input']))
        print('  wsgi.url_sheme    : ' + str(self.environ['wsgi.url_scheme']))
        print('  wsgi.errors       : ' + str(self.environ['wsgi.errors']))
        print('  wsgi.multithread  : ' + str(self.environ['wsgi.multithread']))
        print('  wsgi.multiprocess : ' + str(self.environ['wsgi.multiprocess']))
        print('  wsgi.run_once     : ' + str(self.environ['wsgi.run_once']))
        print("".zfill(100))

    ### the server function, is just a simple make_server from wsgiref.simple_server module ###
    def serve_now(self):
        ### first of all, fill the contain variables with the path to the files ###
        ### in the container folder ###
        self.container_check()
        ### and then, start the server ###
        with make_server('', self.port, self.app) as httpd:
            print("".zfill(100))
            print("0" + f"Valknut is serving on port {self.port}...".center(98) + "0")
            print("0" + "Ctrl-C to shut down the server properly".center(98) + "0")
            if self.debuging == True:
                print("0" + "Debug_environment is activated.".center(98) + "0")
            elif self.debuging == False:
                print("0" + "Debug_environment is desactivated.".center(98) + "0")
            print("".zfill(100))

            ### handling closure for the server ###
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("".zfill(100))
                print("0" + "Valknut server shutting down...".center(98) + "0")
                httpd.shutdown()
                print("0" + "Connection closed !".center(98) + "0")
                print("".zfill(100))
