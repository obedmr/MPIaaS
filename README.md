MPIaaS Project
=================

Requirements
------------
1. VirtualBox
2. Vagrant
3. Python 2.7.x
4. Twisted python package https://pypi.python.org/pypi/Twisted

Initial Setup 
-------------
The above script will start 3 CoreOS VMs by default and will be loading 3 containers on each one. The Container will
have MPI, Python, and SSH enabled. The container flavors are: Ubuntu, Fedora and Archlinux

```
	./setenv.py
	cp ./docker-1.5.0 app/
```

How to run Python in CoreOS Containers
--------------------------------------

```
	cd coreos-vagrant
	vagrant ssh core-01
	docker run -it mpiaas/ubuntu /bin/bash
```

How to run tests
----------------
1. Start the server. (By default it will run the busybox test suite)
```
	cd app/
	python2 mpiaas_runner.py --num_clients 3
```

2. Clients notify the server about their existence
```
	cd coreos-vagrant/
	vagrant ssh core-<client_number[01,02,03]>
	docker run mpiaas/client python2 client --serverip <server_ip> --localip <client_ip> --port <docker_communication_port>
```

3. That's all, the server waits for the 3 clients to subscribe and the the server request the clients to create the containers and then run the busybox test suite.

4. If you want to run lmbench (MPI) you will need to modify the ```app/setup.conf``` and set the test variable to ```mbench```

NOTE:
For more information about the available options in ``` mpiaas_runner.py ``` you can run:
```
	cd app/
	python2 mpiaas_runner.py --help
```

Team
----
- Victor Rodriguez
- Obed N Munoz