#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import threading
import webbrowser
import time
import os

from PyQt4 import QtGui

def handle_server(port, obj, sec):        
   handler = SimpleHTTPServer.SimpleHTTPRequestHandler
   
   try:
      httpd = SocketServer.TCPServer(("", port), handler)
      httpd.timeout = 10
      
      url = "http://%s:%s" % (obj.ip, port)
      obj.statusLbl.setText("Status: %s %s" % ("Start Server", url))        
      webbrowser.open(url)
      
      while obj.isActive:
         try:
            httpd.handle_request()
         except:
            obj.statusLbl.setText("Status: Ups we're  problems")
      
      httpd.server_close()
      obj.statusLbl.setText("Status: Off")

   except:
      for i in range(sec):
         if not obj.isActive: break
         obj.statusLbl.setText("Status: Port busy... wating %s seconds" % (sec - i) )
         time.sleep(1)
      
      if obj.isActive:
         handle_server(port, obj, sec + 5)
      else:
         obj.statusLbl.setText("Status: Off")

         
class GUI(QtGui.QWidget):
    
   def __init__(self):
      super(GUI, self).__init__()
      
      self.initUI()
      
   def __del__(self):
      self.isActive = False
        
   def initUI(self):

      grid = QtGui.QGridLayout()

      self.pathLbl   = QtGui.QLabel("Path: ")
      self.portLbl   = QtGui.QLabel("HTTP port: ")
      self.pathBox   = QtGui.QLineEdit(".")
      self.portBox   = QtGui.QSpinBox()
      self.browseBtn = QtGui.QPushButton("...")
      self.startBtn  = QtGui.QPushButton("Start")
      self.statusLbl = QtGui.QLabel("Status: Off")

      grid.addWidget(self.pathLbl,   0, 0, 1, 1)
      grid.addWidget(self.pathBox,   0, 1, 1, 2)
      grid.addWidget(self.browseBtn, 0, 3, 1, 1)
      grid.addWidget(self.portLbl,   1, 0, 1, 1)
      grid.addWidget(self.portBox,   1, 1, 1, 1)
      grid.addWidget(self.startBtn,  1, 2, 1, 1)
      grid.addWidget(self.statusLbl, 2, 0, 1, 3)

      self.setLayout(grid)   
         
      self.portBox.setMinimum(1025)
      self.portBox.setMaximum(65535)
      self.portBox.setValue(8000)

      self.port = 8000
      self.isActive = False
      self.ip = "127.0.0.1"

      self.browseBtn.pressed.connect(self.selFolder)
      self.startBtn.pressed.connect(self.start)

      self.move(300, 150)
      self.setWindowTitle('PyShare')    
      self.show()

   def selFolder(self):
      self.pathBox.setText(QtGui.QFileDialog.getExistingDirectory())
      
      
   def start(self):        
      if self.isActive == False:
         self.port = int(self.portBox.value())
         self.isActive = True
         
         path_select = self.pathBox.text()        
         os.chdir(path_select)
               
         self.startBtn.setText("Stop")
         
         self.threadserver = threading.Thread(target=handle_server, args=(self.port, self, 10, ))
         self.threadserver.start()
         
      else:            
         self.isActive = False
         self.startBtn.setText("Start")
         self.statusLbl.setText("Status: %s" % ("Stopping Server..."))
         webbrowser.open("http://127.0.0.1:%s" % self.port)

        
def main(): 
   app = QtGui.QApplication(sys.argv)
   ex = GUI()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()

