#!/bin/env python3

import subprocess
import os
import json

DOCKER_TCP=2375

def execute(command):
    """ Bash command helper """
    return subprocess.call(command, shell=True)

def vagrant_up():
    """ Vagrant startup """
    execute("cp user-data coreos-vagrant/")
    execute("cp config.rb coreos-vagrant/")
    execute("cd coreos-vagrant/ ; vagrant up")

def create_containers(virtual=True, clients_count=2, clients=[]):
    """ Creates Linux Containers on Clients """
    if virtual:
        for client in range(1,clients_count + 1):
            clients.append({"host": "localhost", "port": DOCKER_TCP + client})
            
        for client in clients:
            print ("Creating Containers in Client #", client["port"] - DOCKER_TCP)
            os.environ['DOCKER_HOST'] = "tcp://localhost:%d" % client["port"]
            execute("docker pull ubuntu")
    

if __name__ == "__main__":

    config_file = open("config.ini")
    config = json.load(config_file)
    virtual = config["virtual"]["enabled"]

    if virtual:
        vagrant_up()
        
    create_containers()
