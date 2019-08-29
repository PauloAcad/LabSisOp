import time
import BaseHTTPServer
import os


HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        
        #write time
        os.environ['TZ'] = 'UTC+3'
        datahora = os.popen('date').read()
        s.wfile.write("<p>Data e Hora: %s</p>" % datahora)
        
        #uptime
        uptime_file = open("/proc/uptime", "r")
        uptime = uptime_file.read().split()[0]
        s.wfile.write("<p>Uptime: %ss</p>" % uptime)
        uptime_file.close()
        
        #cpu model and speed
        cpu_file = open("/proc/cpuinfo", "r")
        cpu_file_content = cpu_file.read().split("\n")
        model = cpu_file_content[4].split(":")[1]
        speed = cpu_file_content[6].split(":")[1]
        s.wfile.write("<p>CPU Model: %s</p>" % model)
        s.wfile.write("<p>CPU Speed: %s</p>" % speed)
        cpu_file.close()
        
        #cpu load
        stat_f = open("/proc/stat", "r")
        cpu_line = stat_f.split(\n)[0].split()
        load = int(cpu_line[1]) + int(cpu_line[2]) + int(cpu_line[3])
        idle = int(cpu_line[4])
        load_perc = (load / (load_idle)) * 100
        
        

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

