#!/usr/bin/env python
import argparse
import sys
import logging
import ConfigParser
import time
import socket

from test import ThreadingServer

CONFIG_FILE = "config.ini"
CONFIG_CONF = "setup.conf"

GLOBAL_TEST="busybox"
GLOBAL_OS="Ubuntu"
GLOBAL_HW="VM"


def wait_for_clients(counter,delay):
    while counter:
        time.sleep(delay)
        print "Wait for clients"
        counter -= 1

def print_config(args):

    global GLOBAL_TEST
    global GLOBAL_OS
    global GLOBAL_HW

    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if args.show_tests:
        for item in config.items('TESTS'):
            print item
        sys.exit(0)
    if args.show_os:
        for item in config.items('OS'):
            print item
        sys.exit(0)
    if args.show_hw:
        for item in config.items('HW'):
            print item
        sys.exit(0)

    if args.test:
        for item in config.items("TESTS"):
            if item[0] == args.test:
                GLOBAL_TEST=args.test
    if args.os:
        for item in config.items("OS"):
            if item[0] == args.os:
                GLOBAL_OS=args.os
    if args.hw:
        for item in config.items("HW"):
            if item[0] == args.hw:
                GLOBAL_HW=args.hw

    parser = ConfigParser.SafeConfigParser()

    parser.add_section('CONFIG')
    parser.set('CONFIG', 'test',GLOBAL_TEST)
    parser.set('CONFIG', 'os',GLOBAL_OS)
    parser.set('CONFIG', 'hw',GLOBAL_HW)

    parser.write(sys.stdout)
    file_conf = open(CONFIG_CONF,'w')
    parser.write(file_conf)
    file_conf.close()

def main():

    parser = argparse.ArgumentParser(description='Run some funy tests !!')

    group = parser.add_mutually_exclusive_group()

    run_group_list = group.add_mutually_exclusive_group()

    run_group_list.add_argument('--test', action="store", dest="test",\
            help="Test to run")
    run_group_list.add_argument('--os', action="store", dest="os",\
            help="OS to run the tests")
    run_group_list.add_argument('--hw', action="store", dest="hw",\
            help="HW to run the tests")


    info_group_list = group.add_mutually_exclusive_group()

    info_group_list.add_argument("--show_tests",action="store_true",\
            dest="show_tests",help="Show available tests")
    info_group_list.add_argument("--show_os",action="store_true",\
            dest="show_os",help="Show available OS")
    info_group_list.add_argument("--show_hw",action="store_true",\
            dest="show_hw",help="Show available HW")

    try:
        args = parser.parse_args()

        print_config(args)

    except IOError, msg:
        logging.warning("Error in parsing")
        parser.error(str(msg))

    setup = ConfigParser.ConfigParser()
    setup.read(CONFIG_CONF)

    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

    test = setup.get('CONFIG', 'test')
    operating_system = setup.get('CONFIG', 'os')
    hw = setup.get('CONFIG', 'hw')

    cmd = config.get("TESTS",test)

    # if VM , boot VM else send setup to client
    if hw == "VM":
        #start_vms()
        print ("Starting VMS...")
    else:
        print("Running in HW")

    ThreadingServer()
    wait_for_clients(5,2)

if __name__ == "__main__":
    main()
