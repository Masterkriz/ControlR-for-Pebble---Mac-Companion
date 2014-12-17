from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import os

class HTTPRequestHandler(BaseHTTPRequestHandler):

 def do_GET(self):
  if None != re.search('/api/values/*', self.path):
   recordID = int(self.path.split('/')[-1])
   self.send_response(200)
   self.send_header('Content-Type', 'application/json')
   self.end_headers()
   self.wfile.write(recordID)

   _remote_commands = {
    "ITUNES": [
			"""
			osascript -e 'tell application "System Events"
				tell application "iTunes" to activate
			end tell'	
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "iTunes" to activate
				key code 123 using command down
			end tell'		
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "iTunes" to activate
				key code 49
			end tell'		
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "iTunes" to activate
				key code 124 using command down
			end tell'		
			"""
	],
	"KEYNOTE": [
			"""
			osascript -e 'tell application "System Events"
				tell application "Keynote" to activate
			end tell'
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "Keynote" to activate
				key code 123 using command down
			end tell'		
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "Keynote" to activate
				key code 35 using {command down, option down}
			end tell'		
			""",
			"""
			osascript -e 'tell application "System Events"
				tell application "Keynote" to activate
				key code 124 using command down
			end tell'		
			"""
	],
    "POWERPOINT": [
            """
			osascript -e 'tell application "Microsoft PowerPoint"
				activate
            end tell
			""",
            """
            osascript -e 'tell application "Microsoft PowerPoint"
				activate
				go to previous slide slide show view of slide show window 1
            end tell'
            """,
			"""
            osascript -e 'tell application "Microsoft PowerPoint"
				activate
				run slide show slide show settings of active presentation
            end tell'
            """,
            """
            osascript -e 'tell application "Microsoft PowerPoint"
                activate
                go to next slide slide show view of slide show window 1
            end tell'
            """
     ] 
   }

   #### Change command to KEYNOTE, POWERPOINT or ITUNES ###
   cmd = _remote_commands["ITUNES"][recordID]

   os.system(cmd)

  else:
   self.send_response(400, 'Bad Request: record does not exist')
   self.send_header('Content-Type', 'application/json')
   self.end_headers()

  return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
 allow_reuse_address = True
 
 def shutdown(self):
  self.socket.close()
  HTTPServer.shutdown(self)
 
class SimpleHttpServer():
 def __init__(self, ip, port):
  self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
 def start(self):
  self.server_thread = threading.Thread(target=self.server.serve_forever)
  self.server_thread.daemon = True
  self.server_thread.start()
 
 def waitForThread(self):
  self.server_thread.join()
 
 def stop(self):
  self.server.shutdown()
  self.waitForThread()
 
if __name__=='__main__':
 
 server = SimpleHttpServer('', 1337)
 print 'HTTP Server Running...........'
 server.start()
 server.waitForThread()
