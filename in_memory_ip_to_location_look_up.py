#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys 
from os import getcwd, mkdir
from os.path import isdir 
from time import time, ctime  
from ConfigParser import SafeConfigParser
from tornado.options import define, options
from httplib import HTTPConnection 
from model import IPGeo

config_file = 'config.ini' 

def init_server():
	p = SafeConfigParser() 
	p.read(config_file) 
	if p.has_section('global'): 
		server_port = int(p.get('global', 'port'))  
	else:
		server_port = 9998
	define("port", default=server_port, help="run on the given port", type=int)


def buildGeoDB(f):
    p = SafeConfigParser()
    p.read(f)
    mysql_host = p.get('mysql', 'host')
    mysql_user = p.get('mysql', 'user')
    mysql_pass = p.get('mysql', 'password')
    mysql_db   = p.get('mysql' , 'database')
    CacheDB = IPGeo.IPGeoDB(mysql_host, mysql_user, mysql_pass, mysql_db) 
    return CacheDB.RecoverDB() 


class BaseHandler(tornado.web.RequestHandler):
	"""This class was defined to work with tornando async only
	it does not do anything except inheriting from RequestHandler"""
	pass

IPGeoDB = buildGeoDB(config_file) 
class Server(BaseHandler):
    @tornado.web.asynchronous
    def ipToNum(self, ip):
        segments = ip.split(".")
        if len(segments) != 4:
            pass
        num = 0
        for i in range(0, len(segments)):
            num = num << 8 | int(segments[i])
        return num
 
    def remoteLog(self, message):
        scribe_host = p.get('scribe', 'host') 
        scribe_port = p.get('scribe', 'port') 
        catelogy    = p.get('scribe', 'catelogy') 
        logger = ScribeClient(scribe_host, scribe_port) 
        ScribeClient._logToScribe(catelogy, message) 


    def get(self, *args):
        result = ''
        self.write(self.request.remote_ip + "\n")
        for key in IPGeoDB.iterkeys():
            if self.ipToNum(self.request.remote_ip) <= key and self.ipToNum(self.request.remote_ip) >= IPGeoDB[key][0]:
                result = self.write(self.request.remote_ip + "\t" + IPGeoDB[key][1])
                break 
        if result != '': self.write(result) 
        else:
            self.write("Not in DB")
        self.finish() 



def main():
	init_server() 
	tornado.options.parse_command_line()
	webroot = getcwd() + '/' 
	application = tornado.web.Application([
	 			(r'/(.ico)', tornado.web.StaticFileHandler, {'path': webroot}),
        (r'/(.*)', Server),
    ])
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.bind(options.port)
	http_server.start(0)
	tornado.ioloop.IOLoop.instance().start()
	

if __name__ == "__main__":
    main() 
