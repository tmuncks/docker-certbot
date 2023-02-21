#!/usr/bin/env python3
"""
Docker script for certbot

Parameters to `certbot` are passed as the command to the container. This works
exactly as the original `certbot/certbot` image.

When running, certificates are requested and the container exits when done.

It is possible to disable this `oneshot` operation, to have the container
auto-renew certificates nightly at 03:00. This is achieved by setting the
`CERTBOT_ONESHOT` environment variable to `0`.

Environment variables:
  CERTBOT_ONESHOT           Set to 0 to automatically rerun certbot every
                            night at 03:00
"""
import sys
import os
import datetime
import time
import subprocess


def do_certbot(argv):
    """
    Takes care of actually running certbot with the proper parameters
    """
    command = ['certbot'] + list(argv[1:])
    print(f":: Running command: {' '.join(command)}")
    res = subprocess.run(command)
    print(f":: {command[0]}: {res}")


def main(argv):
    """
    Main loop
    """
    do_certbot(argv)
    if os.getenv('CERTBOT_ONESHOT', '1') == '0':
        while True:
            now = datetime.datetime.now()
            renew = now + datetime.timedelta(days=1)
            renew = renew.replace(hour=3, minute=0, second=0, microsecond=0)
            print(f":: Sleeping until: {renew}")
            time.sleep((renew - now).total_seconds())
            do_certbot(argv)


if __name__ == '__main__':
    main(sys.argv)
