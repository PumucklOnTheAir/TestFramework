#!/usr/bin/env python3

from server.server import Server

try:
    Server.start()
except KeyboardInterrupt:
    Server.stop()