FROM rastasheep/ubuntu-sshd
MAINTAINER obed.n.munoz@gmail.com

# Add MPI user
RUN useradd mpiuser
RUN echo "secure\nsecure" | passwd mpiuser
RUN mkdir /home/mpiuser ; chown mpiuser.mpiuser /home/mpiuser 

# Update 
RUN apt-get -y update 

# Install and configure custom software
RUN apt-get -y install mpich python3

# Intall python2 and twisted
RUN apt-get -y install python python-twisted

# Setup ssh keys
RUN mkdir /home/mpiuser/.ssh
COPY ./mpiuser.pub /home/mpiuser/.ssh/authorized_keys
RUN chown -R mpiuser /home/mpiuser/.ssh

# Intall git
RUN apt-get -y install git