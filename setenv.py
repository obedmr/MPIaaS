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

    client_number = port - DOCKER_TCP
    print("Creating Containers in Client #" + str(client_number))
    os.environ['DOCKER_HOST'] = "tcp://%s:%d" % (host, port)
     
    if not os.path.exists('./.tmp'):
        execute("mkdir .tmp")
        execute("./docker-1.5.0 build -t mpiaas/ubuntu dockerfiles/ubuntu")
        execute("./docker-1.5.0 save -o ./.tmp/mpiaas_ubuntu mpiaas/ubuntu")
        execute("./docker-1.5.0 build -t mpiaas/fedora dockerfiles/fedora")
        execute("./docker-1.5.0 save -o ./.tmp/mpiaas_fedora mpiaas/fedora")
        execute("./docker-1.5.0 build -t mpiaas/archlinux dockerfiles/archlinux")
        execute("./docker-1.5.0 save -o ./.tmp/mpiaas_archlinux mpiaas/archlinux")
        #execute("./docker-1.5.0 build -t mpiaas/centos dockerfiles/centos")
        #execute("./docker-1.5.0 save -o ./.tmp/mpiaas_centos mpiaas/centos")
    else:
        execute("./docker-1.5.0 load -i ./.tmp/mpiaas_ubuntu")
        execute("./docker-1.5.0 load -i ./.tmp/mpiaas_fedora")
        execute("./docker-1.5.0 load -i ./.tmp/mpiaas_archlinux")
        #execute("./docker-1.5.0 load -i ./.tmp/mpiaas_centos")


if __name__ == "__main__":

    config_file = open("config.ini")
    config = json.load(config_file)
    virtual = config["virtual"]["enabled"]

    if virtual:
        vagrant_up()

    if virtual:
        clients_count = 3
        for client in range(0, clients_count):
            set_containers("localhost", DOCKER_TCP + client)
