#! /usr/bin/python
from pynosql import client, server

if __name__ == "__main__":
    server().start()
    client().console()