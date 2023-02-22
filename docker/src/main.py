#!/usr/bin/env python3
"""
Docker script for certbot

Parameters to `certbot` are passed as the command to the container. This works
exactly as the original `certbot/certbot` image.

When running, certificates are requested and the container exits when done.

It is possible to disable this `oneshot` operation, to have the container
auto-renew certificates nightly at 03:00. This is achieved by setting the
`CERTBOT_ONESHOT` environment variable to `0`.

Parameters to the dns-powerdns authenticator plugin, can be specified by
setting the `DNS_POWERDNS_API_URL` and `DNS_POWERDNS_API_KEY` environment
variables

Environment variables:
    CERTBOT_ONESHOT             Set to 0 to automatically rerun certbot every
                                night at 03:00
    DNS_POWERDNS_API_URL        Specify value for --dns-powerdns-api-url
    DNS_POWERDNS_API_KEY        Specify value for --dns-powerdns-api-key
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
    command = ['./certbot'] + list(argv)
    print(f":: Running command: {' '.join(command)}")
    res = subprocess.run(command)
    print(f":: {command[0]}: {res}")


def main(argv):
    """
    Main loop
    """
    # handle options
    # any changes to argv is done at the start of the list, to make the generated changes
    # overrideable by command line args
    api_url = os.getenv('DNS_POWERDNS_API_URL')
    api_key = os.getenv('DNS_POWERDNS_API_KEY')
    if api_url and api_key:
        with open("/pdns-credentials-generated.ini", "wt") as f:
            f.write(f"dns_powerdns_api_url = {api_url}\n")
            f.write(f"dns_powerdns_api_key = {api_key}\n")
        argv = ["--dns-powerdns-credentials", "/pdns-credentials-generated.ini"] + argv
        argv = ["--authenticator", "dns-powerdns"] + argv

    # actual certbot loop
    while True:
        do_certbot(argv)
        # exit if oneshot operation
        if os.getenv('CERTBOT_ONESHOT', '1') != '0':
            break
        # sleep until 03:00
        now = datetime.datetime.now()
        renew = now + datetime.timedelta(days=1)
        renew = renew.replace(hour=3, minute=0, second=0, microsecond=0)
        print(f":: Sleeping until: {renew}")
        time.sleep((renew - now).total_seconds())


if __name__ == '__main__':
    # strip the script name off the args list, then pass to main loop
    main(sys.argv[1:])
