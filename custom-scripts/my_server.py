import time
import BaseHTTPServer
import os
import platform
import subprocess


HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

#PEGAR USO DA CPU
'''
Created on 04.12.2014

@author: plagtag
'''
from time import sleep
import sys

class GetCpuLoad(object):
    '''
    classdocs
    '''


    def __init__(self, percentage=True, sleeptime = 1):
        '''
        @parent class: GetCpuLoad
        @date: 04.12.2014
        @author: plagtag
        @info: 
        @param:
        @return: CPU load in percentage
        '''
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        cpu_infos = {} #collect here the information
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            #compute for every cpu
            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                #update dictionionary
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        start = self.getcputime()
        #wait a second
        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load


#END PEGAR USO DA CPU


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
        s.wfile.write("<html><head><title>Target System Information</title></head>")
        
        #write time
        os.environ['TZ'] = 'UTC+3'
        datahora = os.popen('date').read()
        s.wfile.write("<p>Date and time: %s</p>" % datahora)
        
        #uptime
        uptime_file = open("/proc/uptime", "r")
        uptime = uptime_file.read().split()[0]
        s.wfile.write("<p>Uptime: %ss</p>" % uptime)
        
        #cpu model and speed
        cpu_file = open("/proc/cpuinfo", "r")
        cpu_file_content = cpu_file.read().split("\n")
        model = cpu_file_content[4].split(":")[1]
        speed = cpu_file_content[6].split(":")[1]
        s.wfile.write("<p>CPU model: %s</p>" % model)
        s.wfile.write("<p>CPU speed: %s</p>" % speed)
        
        #cpu load
        load = GetCpuLoad().getcpuload()["cpu"]
        s.wfile.write("<p>CPU load: %f %%</p>" % load)        
        
        #memory info
        mem_f = open("/proc/meminfo", "r")
        mem_f = mem_f.read().split("\n")
        mem_total = int(mem_f[0].split()[1])
        mem_free = int(mem_f[1].split()[1])
        mem_used = mem_total - mem_free
        mem_total /= 1000
        mem_used /= 1000        
        s.wfile.write("<p>Total memory: %d MB</p>" % mem_total)
        s.wfile.write("<p>Memory in use: %d MB</p>" % mem_used)
        
        #versao do sistema
        sys_ver = platform.platform()
        s.wfile.write("<p>System version: %s</p>" % sys_ver)
        
        #lista de processos
        list_proc = subprocess.check_output(['ps']).replace('\n','<br>')
        s.wfile.write("<p>Process list: <br> %s</p>" % list_proc)
        
        #end page
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

