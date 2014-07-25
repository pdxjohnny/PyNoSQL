import socket, SocketServer, sys, StringIO, json, os, time, inspect, BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from optparse import OptionParser
from multiprocessing import Process

class client(object):
    HOST, PORT = "localhost", 9999

    def host( self, ip  ):
        self.HOST = ip[0]
        return "Server now at %s:%d" % (self.HOST, self.PORT)

    def port( self, port  ):
        self.PORT = int(port[0])
        return "Server now at %s:%d" % (self.HOST, self.PORT)

    def query( self, send ):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.HOST, self.PORT))
        except:
            return "Couldn't connect to server on %s:%d" % (self.HOST, self.PORT)
        try:
            sock.sendall(send + "\n")
        except:
            return "Couldn't send to server"
        try:
            received = sock.recv(1024)
        except:
            return "No response from server"
        finally:
            sock.close()
        if received:
            return received

    def takeInput( self, text=None ):
        if text:
            userinput = text
        else:
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
        error = self.handleInput( userinput )
        if error:
            print error
            return "Don't query"
        else:
            return " ".join(userinput)

    def handleInput( self, userinput ):
        for method in inspect.getmembers(server(), predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return False
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return getattr(self, method[0])( userinput[1:] )
        return "You have an error in your PySQL syntax";
    
class server(object):
    saveLocation = "./.dbs/"
    myAddress = '0.0.0.0'
    myPort = 9999
    myWebPort = 9998
    connections = {}
    
    def startServer( self ):
        server = SocketServer.TCPServer((self.myAddress, self.myPort), ConnectionHandler)
        print "Serving PySQL on %s:%d" % (self.myAddress, self.myPort)
        server.serve_forever()

    def start( self ):
        p = Process( target=self.startServer )
        p.start()
        w = Process( target=self.startWebServer )
        w.start()

    def startWebServer( self ):
        os.chdir("./.dbs")
        HandlerClass = SimpleHTTPRequestHandler
        ServerClass  = BaseHTTPServer.HTTPServer
        Protocol     = "HTTP/1.0"
        
        server_address = (self.myAddress, self.myWebPort)
        
        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)
        
        sa = httpd.socket.getsockname()
        print "Serving HTTP on %s:%d" % (self.myAddress, self.myWebPort)
        httpd.serve_forever()

    def handleInput( self, userinput ):
        userinput = userinput.split(" ")
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return getattr(self, method[0])( userinput[1:] )
        return "You have an error in your PySQL syntax";
    
    def insert( self, userinput ):
        obj = self.stringToObject(userinput)
        return "OK"
    
    def stringToObject( self, userinput ):
        obj = {};
        for word in userinput:
            try:
                obj[ word.split(":")[0] ] = word.split(":")[1];
            except:
                try:
                    obj[ word.split(":")[0] ] = True;
                except:
                    break
        return obj

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
            if os.path.exists( self.saveLocation + db ):
                return  db + " already exists"
            else:
                os.makedirs( self.saveLocation + db )
                return "Database initialised"
        if userinput[0] == "table":
            if db == "":
                return "Use a database first"
            table = userinput[1];
            if os.path.exists( self.saveLocation + db + "/" + table ):
                return  table + " already exists"
            else:
                file = open( self.saveLocation + db + "/" + table, "w")
                file.close();
                return table + " created"
    
    def show( self, userinput ):
        userinput = self.stringToObject(userinput)
        #return json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))
        if userinput["databases"]:
            if os.path.exists( self.saveLocation ):
                res = os.listdir( self.saveLocation )
            else:
                res = "No database directory, please exicute: configure"
        if userinput[0] == "tables":
            if db == "":
                res = "Use a database first" + "\n"
            if os.path.exists( self.saveLocation + db ):
                res = "Showing tables for " + db + "\n" 
                res += os.listdir( self.saveLocation + db )
            else:
                res = "Database doesn't exist" + "\n"
        return res
    
    def configure( self, userinput ):
        if len(userinput) > 0:
            if userinput[0] == "create":
                os.makedirs( self.saveLocation )
                res = "The database directory " + self.saveLocation + " created"
            elif userinput[0] == "change":
                if len(userinput) >= 2:
                    if os.path.exists( self.saveLocation ):
                        os.system("mv %s %s" % ( self.saveLocation, userinput[1]) )
                    self.saveLocation = userinput[1]
                    res = "The database directory changed to " + self.saveLocation
                else:
                    res = "The database directory is currently " + self.saveLocation
        else:
            if not os.path.exists( self.saveLocation ):
                res = "The database directory " + self.saveLocation + " does not exist do you want to create it or change it?\n" + "configure create, configure change < saveLocation >"
            else:
                res = "Options are create, change"
        return res
    
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
        print self
        self.data = self.request.recv(1024).strip()
        response = server().handleInput( self.data )
        #print response
        self.request.sendall( response )
