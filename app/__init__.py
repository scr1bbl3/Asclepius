#!/bin/python

from flask import Flask
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"
    
@app.route("/10")
def leak_fd_10():
    print "leaking 10FDs\n"
    print os.getcwd()
    # Mode to be set  
  
    # flags 
    flags = os.O_RDWR
    i = 0
    while (i < 1000):
        fd = os.open("/var/www/hitme/file.txt", flags)
        i =  i + 1
        
    return "Oops i did a bad thing - leaked 10 FDs"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
