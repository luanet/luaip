#!/usr/bin/env python
#
# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import shlex
import socket
import subprocess
import time

from flask import Flask, Response, request, send_from_directory


app = Flask(__name__, static_folder='static')

def isOpen(ip, port, protocol):
    s = socket.socket(socket.AF_INET, protocol)
    s.settimeout(0.5)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

@app.route("/")
def icanhazafunction():
    mimetype = "application/json; charset=utf-8"
    result = request.environ['HTTP_X_FORWARDED_FOR']
    ipfs_open = "true" if isOpen(result, 4001, socket.SOCK_STREAM) & isOpen(result, 4001, socket.SOCK_DGRAM) else "false"
    gateway_open = "true" if isOpen(result, 443, socket.SOCK_STREAM) else "false"
    return Response("{\"ip\": \"%s\", \"swarm\": %s, \"gateway\": %s}" % (result, ipfs_open, gateway_open), mimetype=mimetype, headers={"X-Your-Ip": request.remote_addr})

if __name__ == "__main__":
    app.run()
