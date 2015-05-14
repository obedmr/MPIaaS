#!/usr/bin/env python
import argparse
import sys
import logging
import ConfigParser
import time
import socket
import os
import subprocess
import signal

CONFIG_FILE = "config.ini"
CONFIG_CONF = "setup.conf"

GLOBAL_TEST="busybox"
GLOBAL_OS="ubuntu"
GLOBAL_HW="VM"
GLOBAL_NUM_CLIENTS=1
GLOBAL_CLIENTS_ADDR = []


def wait_for_clients(counter,delay):
   
    global GLOBAL_CLIENTS_ADDR

    while counter:

        client_count = 0
        time.sleep(delay)
        print "Wait for clients"
        counter -= 1

        # count the number of clients

        f = open(CONFIG_CONF)
        for line in f:
            if "CLIENT" in line:
                GLOBAL_CLIENTS_ADDR.append(line.split("_")[1].replace("]",""))
                client_count += 1
        f.close()


        if int(client_count) >= int(GLOBAL_NUM_CLIENTS):
            print "We have all the clients we need"
            break

def print_config(args):

    global GLOBAL_TEST
    global GLOBAL_OS
    global GLOBAL_HW
    global GLOBAL_NUM_CLIENTS

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

    if args.num_clients:
            GLOBAL_NUM_CLIENTS=args.num_clients
            print GLOBAL_NUM_CLIENTS

    parser = ConfigParser.SafeConfigParser()

    parser.add_section('CONFIG')
    parser.set('CONFIG', 'test',GLOBAL_TEST)
    parser.set('CONFIG', 'os',GLOBAL_OS)
    parser.set('CONFIG', 'hw',GLOBAL_HW)

    parser.write(sys.stdout)
    file_conf = open(CONFIG_CONF,'w')
    parser.write(file_conf)
    file_conf.close()

def kill_server():
    # kill all the python process
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if 'python' in line:
            print line
            pid = int(line.split(None, 1)[0])
            print pid
            os.kill(pid, signal.SIGKILL)

def main():

    global GLOBAL_CLIENTS_ADDR

    parser = argparse.ArgumentParser(description='Run some funy tests !!')

    group = parser.add_mutually_exclusive_group()

    run_group_list = group.add_mutually_exclusive_group()

    run_group_list.add_argument('--test', action="store", dest="test",\
            help="Test to run")
    run_group_list.add_argument('--os', action="store", dest="os",\
            help="OS to run the tests")
    run_group_list.add_argument('--hw', action="store", dest="hw",\
            help="HW to run the tests")
    run_group_list.add_argument('--num_clients', action="store", dest="num_clients",\
            help="Number of clients to run")

    run_group_list.add_argument('--killserver', action="store_true",
            dest="kill_server",\
            help="Kill the current servers running")

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


    if args.kill_server:
        kill_server()

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

    os.system("python echoserv.py &")

    # wait of clients if they all exist .. exit
    wait_for_clients(20,2)

    # clean array of clients

    GLOBAL_CLIENTS_ADDR = list(set(GLOBAL_CLIENTS_ADDR))
    
    # run command
    for client in GLOBAL_CLIENTS_ADDR:
        print client.strip()

		# set up
        cmd = "export DOCKER_HOST=tcp://%s:2375" % str(client.strip())
        print cmd
        value = "tcp://%s:2375" % str(client.strip())
        os.environ["DOCKER_HOST"] = value

        # Get iamges
        # cmd = "./docker-1.5.0 images | grep mpi | awk '{print $1}'"
        # print cmd
        # os.system(cmd)

        # Start Container
        cmd =  "./docker-1.5.0 run -d -p :10007:22 --name busybox_test mpiaas/%s" % (operating_system)
        print cmd
        os.system(cmd)

		# Remote command execution with ssh
        cmd =  'ssh -F ./ssh_keys/config %s -p 10007  "git clone https://github.com/obedmr/MPIaaS.git "' % str(client.strip())
        print cmd
        os.system(cmd)

        cmd =  'ssh -F ./ssh_keys/config %s -p 10007  "cd MPIaaS/app/tests/%s/ && ./%s.sh"' % (str(client.strip()),str(test),str(test))
        print cmd
        os.system(cmd)

        # Stop and Removal of container
        cmd = "./docker-1.5.0 stop busybox_test"
        print cmd
        os.system(cmd)

        cmd = "./docker-1.5.0 rm busybox_test"
        print cmd
        os.system(cmd)


if __name__ == "__main__":
    main()
