from http.server import BaseHTTPRequestHandler, HTTPServer
import time, sys, base64
from urllib import parse
import json

hostName = "localhost"
serverPort = 8081

class MyServer(BaseHTTPRequestHandler):
    history = []
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if self.getPage() == '/':
            self.wfile.write(("Hello World! " + self.getPage()).encode())
            self.wfile.write(bytes(str(self.getParams()), "utf-8"))
            self.wfile.write(bytes("\nThis is a another line", "utf-8"))
            self.wfile.write(bytes("\n Why does the newline not work, what it pythons newline character. But it doesnt show on the webpage thats weird I think", "utf-8"))
            self.wfile.write(bytes("\n Maybe thats just an unformatted html thing and the newline is working. Thats probably it","utf-8"))
            self.wfile.write(bytes("<br/<br/> Did this work for a line break thingy","utf-8"))
            self.wfile.write(bytes("<br/><br/> yes it seems like it did","utf-8"))
            
            html = open("encryptionBase.html")
            htmlString = html.read()
            html.close()
            self.wfile.write(bytes("<br/><br/>", "utf-8"))
            self.wfile.write(bytes(htmlString.replace("_PLACEHOLDER_", "You have not encrypted or decrypted anything."), "utf-8"))
            #self.wfile.write(bytes("<br/><br/>" + htmlString, "utf-8"))
            
        if self.getPage() == '/encrypt':
            myParams = self.getParams()
            encryptedText = self.encode(myParams['key'], myParams['plaintext'])
            self.wfile.write(encryptedText)
            
        if self.getPage() == '/decrypt':
            myParams = self.getParams()
            decryptedText = self.decode(myParams['key'], myParams['cipherText'])
            self.wfile.write(bytes(decryptedText, "utf-8"))
            
    # Gets the query parameters of a request and returns them as a dictionary
    def getParams(self):
        output = {}
        queryList = parse.parse_qs(parse.urlsplit(self.path).query)
        for key in queryList:
            if len(queryList[key]) == 1:
                output[key] = queryList[key][0]
        return output
    
    # Returns a string containing the page (path) that the request was for
    def getPage(self):           
        return parse.urlsplit(self.path).path
       # return htmlString
    
	# Encode a plaintext using key
    def encode(self, key, plaintext):
        output = []
        for i in range(len(plaintext)):
            key_c = key[i % len(key)]
            enc_c = (ord(plaintext[i]) + ord(key_c)) % 256
            output.append(enc_c)
        return base64.urlsafe_b64encode(bytes(output))
	
	# Decode a ciphertext using key
    def decode(self, key, ciphertext):
        output = []
        ciphertext = base64.urlsafe_b64decode(ciphertext)
        for i in range(len(ciphertext)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ciphertext[i] - ord(key_c)) % 256)
            output.append(dec_c)
        return "".join(output)
            

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at 127.0.0.1:8080")

    try:
        webServer.serve_forever()
    except:
        webServer.server_close()
        print("Server stopped.")
        sys.exit()

    webServer.server_close()
    print("Server stopped.")
    sys.exit()