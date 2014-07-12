#! /usr/bin/python

import socket, sys, StringIO, json, os, time
from multiprocessing import Process
from pysql import client

def main():
    global client
    request = client.takeInput()
    while request:
        received = client.sendRecive( request )
        print "%s" % received
        request = client.takeInput()

if __name__ == "__main__":
    client = client()
    main()