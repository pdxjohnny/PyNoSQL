import socket, SocketServer, sys, StringIO, json, os, time, inspect, BaseHTTPServer, SimpleHTTPServer, shutil, urllib, string, random
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

    def console( self ):
        request = self.takeInput()
        while request:
            if "Don't query" != request:
                received = self.query( request )
                print "%s" % received
            request = self.takeInput()
        sys.exit(0)

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
        if len(userinput) is 0:
           return "Don't query"
        error = self.handleInput( userinput )
        if error:
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
    """
    Server accepts query's in the format of: action {JSON}
    """
    def __init__( self ):
        self.saveLocation = ".dbs/"
        self.myAddress = '0.0.0.0'
        self.myPort = 9999
        self.myWebPort = 9998
        self.connections = {}
    
    def startServer( self ):
        if not os.path.exists( self.saveLocation ):
            os.makedirs( self.saveLocation )
        server = SocketServer.TCPServer((self.myAddress, self.myPort), ConnectionHandler)
        server.serve_forever()

    def start( self ):
        p = Process( target=self.startServer )
        w = Process( target=self.startWebServer )
        p.start()
        w.start()

    def startWebServer( self ):
        HandlerClass = MyHTTPRequestHandler
        ServerClass  = BaseHTTPServer.HTTPServer
        Protocol     = "HTTP/1.0"
        server_address = (self.myAddress, self.myWebPort)
        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)
        sa = httpd.socket.getsockname()
        httpd.serve_forever()

    def handleInput( self, userinput ):
        userinput = userinput.split(" ")
        if os.getcwd().split("/")[-1] == self.saveLocation[:-1]:
            self.saveLocation = "./"
        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0] == userinput[0]:
                return getattr(self, method[0])( userinput[1:] )
        return "You have an error in your PySQL syntax";

    def insert( self, userinput ):
        """
        insert: needs database and table random _id assigned if not specified
        """
        obj = self.stringToObject(userinput)
        if obj.get("database"):
            if obj.get("table"):
                insert = {}
                for value in obj:
                    if value != "database" and value != "table":
                        insert[value] = obj[value]
                self.appendJsonToFile( self.saveLocation + obj.get("database") + "/" + obj.get("table") + ".html" , insert )
                return "OK"
            else:
                return "No table"
        else:
            return "No database"

    def stringToObject( self, userinput ):
        request = " ".join(userinput)
        return json.loads( request )

    def select( self, userinput ):
        """
        select: will return a table if all is true or a single json if _id is given
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("table") and userinput.get("database"):
            if not os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                return "Table or database non-existent"
            if userinput.get("all"):
                with open( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" , 'r') as outfile:
                    output = ""
                    for line in outfile:
                        output += line
                    return '{' + output[:-2] + '}'
            if userinput.get("_id"):
                res = self.loadJsonFromFile( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html", userinput["_id"] )
                if res:
                    return res
                else:
                    return "Not found"
            else:
                return "Select all or by _id"
        else:
            return "Specify database and table"

    def delete( self, userinput ):
        """
        delete: removes a json
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("table") and userinput.get("database"):
            if not os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                return "Table or database non-existent"
            if userinput.get("_id"):
                res = self.removeJsonFromFile( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html", userinput["_id"] )
                if res:
                    return "OK"
                else:
                    return "Not found"
            else:
                return "Delete by _id"
        else:
            return "Specify database and table"

    def update( self, userinput ):
        """
        update: updates a json or creates it if it was not found, updates using _id
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("table") and userinput.get("database"):
            if not os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                return "Table or database non-existent"
            if userinput.get("_id"):
                insert = {}
                for value in userinput:
                    if value != "database" and value != "table":
                        insert[value] = userinput[value]
                res = self.removeJsonFromFile( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html", userinput["_id"] )
                self.appendJsonToFile( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" , insert )
                if res:
                    return "OK"
                else:
                    return "Created"
            else:
                return "Delete by _id"
        else:
            return "Specify database and table"

    def create( self, userinput ):
        """
        creates: creates a table or a database
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("table") and userinput.get("database"):
            if userinput["database"] == True:
                return "Specify a database"
            if os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                return userinput["table"] + " already exists"
            else:
                file = open( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" , "w")
                file.close();
                return "OK"
        elif userinput.get("database"):
            if os.path.exists( self.saveLocation + userinput["database"] ):
                return userinput["database"] + " already exists"
            else:
                os.makedirs( self.saveLocation + userinput["database"] )
                return "OK"
        else:
            return json.dumps( userinput, sort_keys=True, indent=4, separators=(',', ': '))

    def drop( self, userinput ):
        """
        drop: removes a database or a table
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("table") and userinput.get("database"):
            if userinput["database"] == True:
                return "Specify a database"
            if os.path.exists( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" ):
                os.remove( self.saveLocation + userinput["database"] + "/" + userinput["table"] + ".html" )
                return "OK"
            else:
                return userinput["table"] + " doesn't exist"
        elif userinput.get("database"):
            if os.path.exists( self.saveLocation + userinput["database"] ):
                shutil.rmtree( self.saveLocation + userinput["database"] )
                return "OK"
            else:
                return userinput["database"] + " doesn't exist"
        else:
            return json.dumps( userinput, sort_keys=True, indent=4, separators=(',', ': '))

    def show( self, userinput ):
        """
        show: shows all databases or tables of a database
        """
        userinput = self.stringToObject(userinput)
        if userinput.get("tables") and userinput.get("database"):
            if userinput["database"] == True:
                return "Specify a database" + "\n"
            elif os.path.exists( self.saveLocation + userinput["database"] ):
                tables = os.listdir( self.saveLocation + userinput["database"] )
                return json.dumps( tables, sort_keys=True, indent=4, separators=(',', ': ')) 
            else:
                return "Database doesn't exist" + "\n"
        elif userinput.get("databases"):
            if os.path.exists( self.saveLocation ):
                databases = os.listdir( self.saveLocation )
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

    def appendJsonToFile( self, filename, jsonToWrite ):
        f = open(filename,'a');
        if not jsonToWrite.get("_id"):
            alfaNum = string.ascii_lowercase + string.digits
            jsonToWrite["_id"] = ''.join(random.sample(alfaNum*6,20))
        f.write('"%s" : ' % jsonToWrite["_id"]);
        json.dump(jsonToWrite, f);
        f.write(',\n');
        f.close();

    def loadJsonFromFile( self, filename, _id ):
        file = open(filename,'rU');
        for line in file:
            if line.split(":")[0][1:-2] == _id:
                return ':'.join(line.split(":")[1:])[:-2]
        file.close();
        return False;

    def removeJsonFromFile( self, filename, _id ):
        fro = open(filename, "rb")
        res = False
        while True:
            line = fro.readline()
            if not line:
                break
            elif line.split(":")[0][1:-2] != _id:
                seekpoint = fro.tell()
            else:
                print seekpoint
                res = True
                break
        frw = open(filename, "r+b")
        frw.seek(seekpoint, 0)
        chars = fro.readline()
        while chars:
            frw.writelines(chars)
            chars = fro.readline()
        fro.close()
        frw.truncate()
        frw.close()
        return res

class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        try:
            response = server().handleInput( self.data )
        except:
            response = "Server error"
        self.request.sendall( response )

class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*");
        self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
        self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        print self.path
        if self.path.find('?') != -1:
            try:
                request = self.path.split('/')[1][1:]
                request = urllib.unquote_plus( request )
                response = server().handleInput(request)
            except:
                response = "Server Error"
        elif self.path.find('pynosql.js') != -1:
            with open( 'pynosql.js' , 'r') as outfile:
                response = ""
                for line in outfile:
                    response += line
        else:
            response = "<body align='center' style='font:Tahoma, Geneva, sans-serif;color:#707070;'><h1>Welcome to PyNoSQL<hr></h1>"
            for method in inspect.getmembers(server(), predicate=inspect.ismethod):
                try:
                    response += getattr(server(), method[0]).__doc__ + "<br><br>"
                except:
                    pass
            response += "</body>"
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)
        return True

if __name__ == "__main__":
    server().start()