#!/bin/env python3

import subprocess
import os
import json

DOCKER_TCP = 2375

def execute(command):
    """ Bash command helper """
    return subprocess.call(command, shell=True)


def vagrant_up():
    """ Vagrant startup """
    if not os.path.exists("./docker-1.5.0"):
        execute("wget https://get.docker.com/builds/Linux/x86_64/docker-1.5.0")
        execute("chmod 755 ./docker-1.5.0")
    if not os.path.exists("coreos-vagrant"):
        execute("git clone https://github.com/coreos/coreos-vagrant.git")
    execute("cp user-data coreos-vagrant/")
    execute("cp config.rb coreos-vagrant/")
    execute("cd coreos-vagrant/ ; vagrant up")


def set_containers(host, port):
    """ Creates Linux Containers on Client """

    client_number = port - DOCKER_TCP + 1
    print("Creating Containers in Client #" + str(client_number))
    base_url = "tcp://%s:%d" % (host, port)
    os.environ['DOCKER_HOST'] = base_url
    images = ['ubuntu', 'archlinux', 'fedora']

    for image in images:
        if (not os.path.exists('.tmp_mpiaas_%s' % image )):
            execute("./docker-1.5.0 build -t mpiaas/%s dockerfiles/%s"
                    % ( image, image ) )
            execute("./docker-1.5.0 save -o .tmp_mpiaas_%s mpiaas/%s"
                    % ( image, image ) )
        else:
            execute("./docker-1.5.0 load -i .tmp_mpiaas_%s"
                    % image )


def main():
    pass

if __name__ == "__main__":

    config_file = open("config.ini")
    config = json.load(config_file)
    virtual = config["virtual"]["enabled"]

    if virtual:
        vagrant_up()
        clients_count = 3
        for client in range(0, clients_count):
            set_containers("localhost", DOCKER_TCP + client)
