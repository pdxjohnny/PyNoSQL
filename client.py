#! /usr/bin/python

import socket, sys, StringIO, json, os, time
from multiprocessing import Process
from pysql import client

def main():
    global client
    if len(sys.argv) > 1:
        request = client.takeInput( sys.argv[1:] )
        while request:
            if "Don't query" != request:
                received = client.query( request )
                print "%s" % received
            request = client.takeInput()
    else:
        print client.query( "configure create" )

if __name__ == "__main__":
    client = client()
    main()