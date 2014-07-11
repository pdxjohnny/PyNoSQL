#! /usr/bin/python

import socket
import sys
from server import transfer

def main():
	transfer().send( "/home/johnny/Documents/test/client/test1.txt" )

if __name__ == "__main__":
    main()