import socket, SocketServer, sys, StringIO, json, os, time, inspect
from optparse import OptionParser
from multiprocessing import Process

class client(object):
    HOST, PORT = "localhost", 9999

    def sendRecive( self, send ):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to server and send send
            sock.connect((self.HOST, self.PORT))
            sock.sendall(send + "\n")
        
            # Receive data from the server and shut down
            received = sock.recv(1024)
        finally:
            sock.close()
        return received

    def takeInput( self ):
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
            return userinputString

class server(object):
    myAddress = '0.0.0.0'
    myPort = 9999
    connections = {}
    
    def startServer( self ):
        server = SocketServer.TCPServer((self.myAddress, self.myPort), ConnectionHandler)
        server.serve_forever()

    def start( self ):
        p = Process( target=self.startServer )
        p.start()

    def handleInput( self, userinput ):
        userinput = userinput.split(" ")
        error = True
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return getattr(self, method[0])( userinput[1:] )
        return "You have an error in your PySQL syntax";
    
    def insert( self, userinput ):
        obj = {};
        for word in userinput:
            obj[ word.split(":")[0] ] = word.split(":")[1];
        return "OK"

    def select( self, userinput ):
        if userinput[0] == "all":
            printObject(user);
        elif userinput[0] in user:
            print(user[userinput[0]]);
        else:
            print("Sorry that JSON is not in memory");
    
    def create( self, userinput ):
        if userinput[0] == "database":
            db = userinput[1];
            if os.path.exists("dbs/"+db):
                print( db + " already exists" )
            else:
                os.makedirs("dbs/"+db)
                print("Database initialised")
        if userinput[0] == "table":
            if db == "":
                print("Use a database first")
                return False;
            table = userinput[1];
            if os.path.exists("dbs/"+db+"/"+table):
                print( table + " already exists" )
            else:
                file = open("dbs/"+db+"/"+table, "w")
                file.close();
                print(table+" created")
    
    def show( self, userinput ):
        if userinput[0] == "databases":
            if os.path.exists("dbs/"):
                printArray( os.listdir("dbs/") )
        if userinput[0] == "tables":
            if db == "":
                print("Use a database first")
                return False;
            if os.path.exists("dbs/"+db):
                print("Showing tables for "+db)
                printArray( os.listdir("dbs/"+db) )
            else:
                print("Database doesn't exist")
    
    def printObj( self, obj ):
        if isinstance(obj, dict):
            printObject(obj)
        if isinstance(obj, list):
            printArray(obj)
    
    def printObject( self, obj ):
        for i in obj:
            if isinstance(obj[i], dict):
                print(i);
                printObject(obj[i])
            else:
                print("\t"+i+": "+str(obj[i]) );
    
    def printArray( self, array ):
        for i in array:
            if isinstance(i, list):
                print(i);
                printArray(array[i])
            else:
                print("\t"+i);
    
    def writeObject( self, file, jsonName, obj ):
        f = open(file,'a');
        f.write(jsonName+"-->");
        for i in obj:
            if isinstance(obj[i], dict):
                writeObject(file, obj[i]);
            else:
                json.dump(obj, f);
                f.write('\n');
                f.close();
                return True;
        f.close();
    
    def writeJsonToFile( self, file, jsonToWrite ):
        f = open(file,'w');
        json.dump(jsonToWrite, f);
        f.close();
    
    def appendJsonToFile( self, file, jsonToWrite ):
        f = open(file,'a');
        f.write('\n');
        json.dump(jsonToWrite, f);
        f.write('\n');
        f.close();
    
    def loadJsonsFromFile( self, filename, array ):
        file = open(filename,'rU');
        for line in file:
            name = line.split("-->")[0];
            obj = line.split("-->")[1][0:-1];
            while contains(array, name):
                name += "1"
            array[name] = json.loads(obj);
        file.close();
        return array;
    
    def contains( self, obj, string ):
        if obj.get(string):
            return True;
        else:
            return False;

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        server().handleInput( self.data )
        self.request.sendall( server().handleInput( self.data ) )
