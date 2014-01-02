#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Check external IP changes.
"""

import os
import sys
import urllib
import socket

# keeps track of the last updated IP
IP_FILE = os.path.join(os.path.expanduser('~'), '.ipcheck')

class IpChangedError(Exception): pass


def get_current_ip():
    """Get the current external IP."""
    return urllib.urlopen("http://myip.dnsdynamic.org/").read()

def get_last_ip():
    """Get the last checked external IP."""
    if not os.path.exists(IP_FILE):
        return None
    with open(IP_FILE) as f:
        return f.read()

def check_ip():
    """Raises an IpChangedError exception if the IP was changed."""
    current_ip = get_current_ip()
    if current_ip != get_last_ip():
        with open(IP_FILE, "w") as f:
            f.write(current_ip)
        msg = "External IP updated for host {0}: {1}".format(socket.gethostname(), current_ip)
        raise IpChangedError(msg)

def main():
    """Main program."""
    try:
        check_ip()
    except Exception, msg:
        return msg

if __name__ == '__main__':
    sys.exit(main())
