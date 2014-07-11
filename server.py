#! /usr/bin/python

import socket, sys, StringIO, json, os, time

class transfer(object):
    serverAddress = "localhost"
    serverPort = 9999
    myAddress = "localhost"
    myPort = 9999
    connections = {'self': myAddress, }
    def sendFile( self, fileLocation ):
        s = socket.socket()
        s.connect( ( self.serverAddress, self.serverPort ) )
        f=open (fileLocation, "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        s.close()

    def sendText( self, text ):
        s = socket.socket()
        s.connect( ( self.serverAddress, self.serverPort ) )
        for char in text:
            s.send(char)
        s.close()
    
    def reciveFile( self, saveLocation="./", onComplete=None, onCompleteParam=None ):
        s = socket.socket()
        s.bind( ( self.myAddress, self.myPort ) )
        s.listen(10)
        while True:
            sc, address = s.accept()
            i = 0
            fileName = saveLocation+'file_'+ str(i)
            f = open( fileName,'wb')
            i += 1
            while (True):       
                l = sc.recv(1024)
                while (l):
                    f.write(l)
                    l = sc.recv(1024)
                break
            f.close()
            if onComplete:
                if onCompleteParam:
                    onComplete( fileName, onCompleteParam )
                else:
                    onComplete( fileName )
            sc.close()
            s.close()
            return address, fileName
    
    def reciveText( self, saveLocation="./", onComplete=None, onCompleteParam=None ):
        s = socket.socket()
        s.bind( ( self.myAddress, self.myPort ) )
        s.listen(10)
        while True:
            sc, address = s.accept()
            text = StringIO.StringIO()
            while (True):
                l = sc.recv(1024)
                while (l):
                    text.write(l)
                    l = sc.recv(1024)
                request = text.getvalue()
                text.close()
                sc.close()
                s.close()
                return address, request

def addToFile( path, text="Addition to file" ):
    f = open( path,'a')
    f.write(text)
    f.close()
    print( "Done writing file "+fileName )

def main():
    global transfer
    print "Starting server bound to "+transfer.myAddress+" on port "+str(transfer.myPort)
    while ( True ):
        (address, fileName) = transfer.reciveText()
        transfer.serverAddress = address[0]
        print address[0]+" requested "+fileName
        time.sleep(1)
        transfer.sendFile( "/home/johnny/Documents/test/server/"+fileName )


if __name__ == "__main__":
    transfer = transfer()
    transfer.serverPort = 9998
    main()