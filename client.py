#! /usr/bin/python

import socket, sys, StringIO, json, os, time
from multiprocessing import Process
from pynosql import client

def main():
    global client
    if sys.argv[1] != "run":
        request = client.takeInput( sys.argv[1:] )
        while request:
            if "Don't query" != request:
                received = client.query( request )
                print "%s" % received
            request = client.takeInput()
    else:
        print client.query( "use test" )
        print client.query( "show tables" )
        table = client.query( "select all table:table" )
        print table
        table = json.loads( table )
        print json.dumps(table, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    client = client()
    main()