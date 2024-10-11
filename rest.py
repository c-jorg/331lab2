# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json
from urllib import parse
from json import JSONDecodeError

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    
    myDict = {}
    
    # You can pass an integer statusCode (i.e. 200, 404, etc) to this function to return a specific HTTP status
    def set_headers(self, statusCode):
        self.send_response(statusCode)
        self.send_header("Content-type", "text/html")
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        self.send_header('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, PATCH, OPTIONS")
        self.end_headers()
    
    def do_GET(self):
        print("GET REQUEST")
        
        myURI = self.getURI()
        

        
        if myURI == "/":
            self.set_headers(200)
            self.wfile.write(self.getURI().encode())
            html = open("request.html")
            htmlString = html.read()
            html.close()
            self.wfile.write(bytes(htmlString, "utf-8"))
       
        if myURI in self.myDict:
           params = self.getParams()
           
           if 'key' in params:
               jsonKey = params['key']
               if jsonKey in self.myDict[myURI]:
                   data = self.myDict[myURI][jsonKey]
                   self.set_headers(200)
                   self.wfile.write(str(data).encode())
               else:
                   self.set_headers(404)
           else:
               self.set_headers(200)
               self.wfile.write(str(self.myDict[myURI]).encode())
        else:
           self.set_headers(404)

        
    def do_POST(self):
        print("POST REQUEST")
        #TO-DO: CREATE JSON OBJECT
        
        myURI = self.getURI()
        if myURI not in self.myDict:
            try:
                data = json.loads(self.getBody())
                self.myDict[myURI] = data
                self.set_headers(201)
            except:
                self.set_headers(400)
        else:
            self.set_headers(409)
        
    def do_PUT(self):
        print("PUT REQUEST")
        # TO-DO: OVERWRITE EXISTING JSON OBJECT
        
        myURI = self.getURI()
       # print(myURI)
        if myURI in self.myDict:
            params = self.getParams()
            try:
                data = json.loads(self.getBody())
                if 'key' in params:
                    print("key in params")
                    jsonKey = params['key']
                    if jsonKey in self.myDict[myURI]:
                        del self.myDict[myURI][jsonKey]
                        self.set_headers(200)
                        self.myDict[myURI] = data
                        self.wfile.write(str(data).encode())
    
                        self.set_headers(400)
                else:
                    print("key not in params")
                    self.set_headers(200)
                    self.wfile.write(str(data).encode())
                    del self.myDict[myURI]
                    self.myDict[myURI] = data
            except:
                self.set_headers(400)
        else:
            self.set_headers(404)
        
    def do_DELETE(self):
        print("DELETE REQUEST")
        # TO-DO: DELETE EXISTING JSON OBJECT
        
        myURI = self.getURI()
        if myURI in self.myDict:
            params = self.getParams()

            if 'key' in params:
                jsonKey = params['key']
                if jsonKey in self.myDict[myURI]:
                    try:
                        data = self.myDict[myURI][jsonKey]
                        del self.myDict[myURI][jsonKey]
                        self.set_headers(200)
                        self.wfile.write(str(data).encode())
                    except:
                        self.set_headers(400)
            else:
                self.set_headers(200)
                self.wfile.write(str(self.myDict[myURI]).encode())
                del self.myDict[myURI]
        else:
            self.set_headers(404)
            
        
    def do_PATCH(self):
        print("PATCH REQUEST")
        # TO-DO: SELECTIVELY OVERWRITE KEY-VALUE PAIRS OF A JSON OBJECT
        
        self.do_PUT()
        #remove this when patch actually works
        
        myURI = self.getURI()
        if myURI in self.myDict:
            params = self.getParams()
            
            
        else:
            self.set_headers(404)
        
    # This is necessary, as OPTIONS is used to check if the service supports HTTP 1.1 verbs (PUT, PATCH, DELETE)    
    def do_OPTIONS(self):
        self.set_headers(200)
        
    # This function retrieves the current URI that has been requested by the client   
    def getURI(self):
        return parse.urlsplit(self.path).path
    
    # This function gets any query string parameters that were part of the request
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    # This function retrieves the request body data
    def getBody(self):
        return self.rfile.read(int(self.headers.get('Content-Length')))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    webServer.serve_forever()