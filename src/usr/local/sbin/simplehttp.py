#!/usr/bin/python
import signal
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import sep,fstat
import sys
import shutil
import datetime
import ConfigParser
filename = '/usr/local/etc/simplehttp.ini'
sys.stdout = open("/var/log/simplehttp/out.log","a")
sys.stderr = open("/var/log/simplehttp/error.log","a")

try:
    config = ConfigParser.ConfigParser()
    config.read(filename)
    PORT_NUMBER = int(config.get('simplehttp','PORT'))
except :
    PORT_NUMBER = 7979

DIRECTORY = "/var/lib/jelastic/backup/export"

def signal_term_handler(signal, frame):
    today = datetime.datetime.today().strftime("%a, %d %b %Y %X")
    print today, "- - got SIGTERM"
    sys.stdout.flush()
    server.socket.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)

class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
	self.error_message_format='<head><title>Error response</title></head><body><h1>Error response</h1><p>Error code %(code)d.<p>%(explain)s.</body>'
        try:
            if self.path.endswith(".tar.gz"):
                mimetype='application/x-gzip'
                f = open(DIRECTORY + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type',mimetype)
		size = fstat(f.fileno()).st_size
                self.send_header('Content-Length', size)
		self.end_headers()
                print "%s 200 - %s - %s" %( self.date_time_string(), self.headers.getheaders("X-Real-IP"), self.requestline )
                sys.stdout.flush()
		if self.command == "HEAD":
			f.close
			return
		shutil.copyfileobj(f, self.wfile)
                f.close
            else:
                self.send_error(404,'File Not Found: %s' % self.path)
                print "%s 404 - %s - %s - wrong file request" %( self.date_time_string(), self.headers.getheaders("X-Real-IP"), self.requestline )
                sys.stdout.flush()
            return

        except IOError:
	    self.send_error(404,'File Not Found: %s' % self.path)
	    print "%s 404 - %s - %s" %( self.date_time_string(), self.headers.getheaders("X-Real-IP"), self.requestline )
            sys.stdout.flush()

    def do_HEAD(self):
	self.do_GET()
	return

if __name__ == '__main__':
    try:
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()

