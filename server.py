#! /usr/bin/python

import socket, SocketServer, sys, StringIO, json, os, time, inspect
from optparse import OptionParser
from multiprocessing import Process
from pysql import server

def main():
    server().start()

if __name__ == "__main__":
    main()
