import socket, SocketServer, sys, StringIO, json, os, time, inspect, BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from optparse import OptionParser
from multiprocessing import Process

class client(object):

    def __init__( self ):
        self.HOST = "localhost"
        self.PORT = 9999
        self.database = None

    def use( self, database ):
        self.database = database[0]
        return "Using database " + self.database

    def host( self, ip  ):
        self.HOST = ip[0]
        return "Server now at %s:%d" % (self.HOST, self.PORT)

    def port( self, port  ):
        self.PORT = int(port[0])
        return "Server now at %s:%d" % (self.HOST, self.PORT)

    def query( self, send ):
        text = self.handleInput( send.split(" ") )
        if text:
            return text
        if self.database and "show" in send.split(" ") \
            or "insert" in send.split(" ") or "select" in send.split(" "):
            if send[-1] is ' ':
                send += "database:" + self.database
            else:
                send += " database:" + self.database
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

    def takeInput( self, text=None, user=True ):
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
            if user:
                print error
            return "Don't query"
        else:
            return " ".join(userinput)

    def handleInput( self, userinput ):
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return getattr(self, method[0])( userinput[1:] )
        for method in inspect.getmembers(server(), predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return False
        return "You have an error in your PySQL syntax";        

class server(object):
    def __init__( self ):
        self.saveLocation = "./.dbs/"
        self.myAddress = '0.0.0.0'
        self.myPort = 9999
        self.myWebPort = 9998
        self.connections = {}
        if not os.path.exists( self.saveLocation ):
            os.makedirs( self.saveLocation )
    
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
        os.chdir( self.saveLocation )
        HandlerClass = SimpleHTTPRequestHandler
        ServerClass  = BaseHTTPServer.HTTPServer
        Protocol     = "HTTP/1.0"
        
        server_address = (self.myAddress, self.myWebPort)
        
        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)
        
        sa = httpd.socket.getsockname()
        databases = os.listdir( "./" )
        if len(databases) > 0 and "index.html" in databases:
            del databases[databases.index("index.html")]
        with open( "index.html" , 'w') as outfile:
            json.dump( databases, outfile)
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
        if obj.get("database"):
            if obj.get("table"):
                insert = {}
                for value in obj:
                    if value != "database" and value != "table":
                        insert[value] = obj[value]
                print insert
                self.appendJsonToFile( self.saveLocation + obj.get("database") + "/" + obj.get("table") + ".html" , insert )
            else:
                return "No table"
        else:
            return "No database"
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
        userinput = self.stringToObject(userinput)
        print json.dumps(userinput, sort_keys=True, indent=4, separators=(',', ': '))
        if userinput.get("table") and userinput.get("database"):
            if userinput.get("all"):
                with open( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" , 'r') as outfile:
                    output = ""
                    for line in outfile:
                        output += line
                    return '[' + output[:-2] + ']'
        else:
            return "Specify database and table"

    def create( self, userinput ):
        userinput = self.stringToObject(userinput)
        print json.dumps(userinput, sort_keys=True, indent=4, separators=(',', ': '))
        if userinput.get("table") and userinput.get("database"):
            if userinput["database"] == "":
                return "Specify a database"
            if os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                return userinput["table"] + " already exists"
            else:
                file = open( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" , "w")
                file.close();
                tables = os.listdir( self.saveLocation + userinput["database"] )
                if len(tables) > 0 and "index.html" in tables:
                    del tables[tables.index("index.html")]
                with open( self.saveLocation + userinput["database"] + "/index.html" , 'w') as outfile:
                    json.dump( tables, outfile)
                return userinput["table"] + " created"
        elif userinput.get("database"):
            if os.path.exists( self.saveLocation + userinput["database"] ):
                return userinput["database"] + " already exists"
            else:
                os.makedirs( self.saveLocation + userinput["database"] )
                databases = os.listdir( self.saveLocation )
                if len(databases) > 0 and "index.html" in databases:
                    del databases[databases.index("index.html")]
                with open( self.saveLocation + "index.html" , 'w') as outfile:
                    json.dump( databases, outfile)
                tables = os.listdir( self.saveLocation + userinput["database"] )
                if len(tables) > 0 and "index.html" in tables:
                    del tables[tables.index("index.html")]
                with open( self.saveLocation + userinput["database"] + "/index.html" , 'w') as outfile:
                    json.dump( tables, outfile)
                return json.dumps( {userinput["database"]:True}, sort_keys=True, indent=4, separators=(',', ': '))

    def show( self, userinput ):
        userinput = self.stringToObject(userinput)
        print json.dumps(userinput, sort_keys=True, indent=4, separators=(',', ': '))
        if userinput.get("tables") and userinput.get("database"):
            if userinput["database"] == True:
                return "Specify a database" + "\n"
            elif os.path.exists( self.saveLocation + userinput["database"] ):
                tables = os.listdir( self.saveLocation + userinput["database"] )
                if "index.html" in tables:
                    del tables[tables.index("index.html")]
                with open( self.saveLocation + userinput["database"] + "/index.html" , 'w') as outfile:
                    json.dump( tables, outfile)
                return json.dumps( tables, sort_keys=True, indent=4, separators=(',', ': ')) 
            else:
                return "Database doesn't exist" + "\n"
        elif userinput.get("databases"):
            if os.path.exists( self.saveLocation ):
                databases = os.listdir( self.saveLocation )
                if "index.html" in databases:
                    del databases[databases.index("index.html")]
                with open( self.saveLocation + "index.html" , 'w') as outfile:
                    json.dump( databases, outfile)
                return json.dumps( databases, sort_keys=True, indent=4, separators=(',', ': '))
            else:
                return "No database directory, please exicute: configure"
        else:
            return "Usage, show tables database:example, show databases"

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

    def appendJsonToFile( self, filename, jsonToWrite ):
        f = open(filename,'a');
        json.dump(jsonToWrite, f);
        f.write(',\n');
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
