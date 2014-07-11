#! /usr/bin/python

import socket
import sys

class transfer(object):
    serverAddress = "localhost"
    serverPort = 9999
    def send( self, fileLocation ):
        s = socket.socket()
        s.connect( ( self.serverAddress, self.serverPort ) )
        f=open (fileLocation, "rb") 
        l = f.read(1024)
        while (l):
           s.send(l)
           l = f.read(1024)
        s.close()
    
    def recive( self, saveLocation="./", onComplete=None ):
        s = socket.socket()
        s.bind( ( self.serverAddress, self.serverPort ) )
        s.listen(10)
        while True:
            sc, address = s.accept()
            print address
            i = 0
            fileName = saveLocation+'file_'+ str(i)+".txt"
            f = open( fileName,'wb')
            i += 1
            while (True):       
                l = sc.recv(1024)
                while (l):
                    f.write(l)
                    l = sc.recv(1024)
                break
            print( "Done writing file "+fileName )
            f.close()
            if onComplete:
                onComplete( fileName )
            sc.close()
        s.close()

def addToFile( path ):
    f = open( path,'a')
    f.write("Hey I got the file")
    f.close()

def main():
    transfer().recive( "/home/johnny/Documents/test/server/", addToFile )

if __name__ == "__main__":
    main()