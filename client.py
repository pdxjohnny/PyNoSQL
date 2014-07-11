#! /usr/bin/python

import socket, sys, StringIO, json, os, time
from server import transfer

def main():
    global transfer;
    while takeInput() is True:
        pass

def takeInput():
    global transfer;
    userinputString = raw_input('#: ');
    userinput = userinputString.split()
    if "exit" in userinput:
        if userinput.index("exit") is 0:
            print("Bye");
            return False;
    elif "logout" in userinput:
        if userinput.index("logout") is 0:
            print("Bye");
            return False;
    else:
        transfer.sendText( userinputString )
        if transfer.reciveFile( "/home/johnny/Documents/test/client/", readFile ):
            return True

def readFile( fileName ):
    file = open( fileName, "rb" )
    for line in file:
        print( line )
    file.close()

if __name__ == "__main__":
    transfer = transfer()
    transfer.myPort = 9998
    main()