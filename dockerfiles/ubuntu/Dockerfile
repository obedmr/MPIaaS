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
