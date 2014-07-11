#! /usr/bin/python

import socket, sys, StringIO, json, os, time

class transfer(object):
    serverAddress = "localhost"
    serverPort = 9999
    myAddress = "localhost"
    myPort = 9999
    connections = {}

    def sendFile( self, fileLocation ):
        s = socket.socket()
        s.connect( ( self.serverAddress, self.serverPort ) )
        f=open (fileLocation, "rb") 
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)
        s.close()

    def sendText( self, text ):
        s = socket.socket()
        s.connect( ( self.serverAddress, self.serverPort ) )
        for char in text:
            s.send(char)
        s.close()
    
    def reciveFile( self, saveLocation="./", onComplete=None, onCompleteParam=None ):
        s = socket.socket()
        s.bind( ( self.myAddress, self.myPort ) )
        s.listen(10)
        while True:
            sc, address = s.accept()
            i = 0
            fileName = saveLocation+'file_'+ str(i)
            f = open( fileName,'wb')
            i += 1
            while (True):       
                l = sc.recv(1024)
                while (l):
                    f.write(l)
                    l = sc.recv(1024)
                break
            f.close()
            if onComplete:
                if onCompleteParam:
                    onComplete( fileName, onCompleteParam )
                else:
                    onComplete( fileName )
            sc.close()
            s.close()
            return address, fileName
    
    def reciveText( self, onComplete=None, onCompleteParam=None ):
        s = socket.socket()
        s.bind( ( self.myAddress, self.myPort ) )
        s.listen(10)
        while True:
            sc, address = s.accept()
            self.connections[address[0]] = {}
            text = StringIO.StringIO()
            while (True):
                l = sc.recv(1024)
                while (l):
                    text.write(l)
                    l = sc.recv(1024)
                request = text.getvalue()
                text.close()
                if onComplete:
                    if onCompleteParam:
                        onComplete( sc, request, onCompleteParam )
                    else:
                        onComplete( sc, request )
                sc.close()
                s.close()
                return address, request

class PySQL_Server(object):
    def handleInput( self, connectionServer, userConnectionId, userinput ):
        slef.user[user], db = user['db'], table = user['table'];
        if "insert" in userinput and userinput.index("insert") is 0:
            pre = userinput[2:];
            obj = {};
            for i in pre:
                obj[i.split(":")[0]] = i.split(":")[1];
            print(userinput[1])
            printObject(obj)
            self.user[userinput[1]] = obj;
        elif "use" in userinput and userinput.index("use") is 0:
            db = userinput[1];
            if os.path.exists("dbs/"+db):
                print("Database "+userinput[1]+" contains:")
                printArray( os.listdir("dbs/"+db) )
            else:
                print("Database doesn't exist")
        elif "create" in userinput and userinput.index("create") is 0:
            create(userinput[1:])
        elif "show" in userinput and userinput.index("show") is 0:
            show(userinput[1:])
        elif "select" in userinput and userinput.index("select") is 0:
            select(userinput[1:])
        elif "save" in userinput and userinput.index("save") is 0:
            if userinput[1] == "all":
                f = open(userinput[2] , 'w');
                f.close();
                for i in user:
                    writeObject(userinput[2], i, self.user[i]);
            elif userinput[1] in user:
                writeObject(userinput[2], userinput[1], self.user[userinput[1]]);
            else:
                print("Sorry no JSONs in memory");
        elif "delete" in userinput and userinput.index("delete") is 0:
            if userinput[1] == "all":
                user = {};
            elif userinput[1] in user:
                del self.user[userinput[1]];
            else:
                print("Sorry that JSON is not in memory");
        elif "load" in userinput and userinput.index("load") is 0:
            print( "Loading JSONs from " + userinput[1] );
            loadJsonsFromFile(userinput[1], user);
            printObject(user);
        elif "modify" in userinput and userinput.index("modify") is 0:
            print( "Modifing " + userinput[1] + ", currently: " );
            printObject(self.user[userinput[1]])
            change = input(userinput[1]+": ").split();
            self.user[userinput[1]][change[0]] = change[1];
        else:
            return 0;
    
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

def main():
    global transfer, py_server
    print "Starting server bound to "+transfer.myAddress+" on port "+str(transfer.myPort)
    while ( True ):
        (address, request) = transfer.reciveText( py_server.handleInput )
        transfer.serverAddress = address[0]
        print address[0]+"\tsent:\t "+request
        time.sleep(1

if __name__ == "__main__":
    transfer = transfer()
    py_server = PySQL_Server()
    transfer.serverPort = 9998
    main()
