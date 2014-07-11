#! /usr/bin/python

import socket, sys, StringIO, json, os
from server import transfer

def main():
    handleInput(sys.argv[1:])
    while takeInput() is True:
        pass

def takeInput():
    global user;
    userinput = input('#: ');
    userinput = userinput.split();
    if "exit" in userinput:
        if userinput.index("exit") is 0:
            print("Bye");
            return False;
    elif "logout" in userinput:
        if userinput.index("logout") is 0:
            print("Bye");
            return False;
    handleInput(userinput);
    return True;

def readFile( fileName ):
    file = open( fileName, "rb" )
    for line in file:
        print( line )
    file.close()

def handleInput(userinput):
    #global user;
    #global db;
    #global table;
    global transfer;
    if "file" in userinput and userinput.index("file") is 0:
        transfer.sendText( userinput[1] )
        if transfer.reciveFile( "/home/johnny/Documents/test/client/", readFile ):
            return True
    elif "insert" in userinput and userinput.index("insert") is 0:
        pre = userinput[2:];
        obj = {};
        for i in pre:
            obj[i.split(":")[0]] = i.split(":")[1];
        print(userinput[1])
        printObject(obj)
        user[userinput[1]] = obj;
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
                writeObject(userinput[2], i, user[i]);
        elif userinput[1] in user:
            writeObject(userinput[2], userinput[1], user[userinput[1]]);
        else:
            print("Sorry no JSONs in memory");
    elif "delete" in userinput and userinput.index("delete") is 0:
        if userinput[1] == "all":
            user = {};
        elif userinput[1] in user:
            del user[userinput[1]];
        else:
            print("Sorry that JSON is not in memory");
    elif "load" in userinput and userinput.index("load") is 0:
        print( "Loading JSONs from " + userinput[1] );
        loadJsonsFromFile(userinput[1], user);
        printObject(user);
    elif "modify" in userinput and userinput.index("modify") is 0:
        print( "Modifing " + userinput[1] + ", currently: " );
        printObject(user[userinput[1]])
        change = input(userinput[1]+": ").split();
        user[userinput[1]][change[0]] = change[1];
    else:
        return 0;

if __name__ == "__main__":
    transfer = transfer()
    main()