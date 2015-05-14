FROM kumarpraveen/fedora-sshd
MAINTAINER obed.n.munoz@gmail.com

# Add MPI user
RUN useradd mpiuser
RUN echo -e "secure\nsecure" | passwd mpiuser

# Update
RUN yum clean metadata
RUN yum clean all
RUN yum makecache fast
RUN yum -y update --nogpgcheck


# Install and configure custom software
RUN yum clean all
RUN yum -y install mpich python3 --nogpgcheck

# Add mpich to PATH
RUN echo "PATH=$PATH:/usr/lib64/mpich/bin" >> /etc/profile

# Install twisted
RUN yum clean all
RUN yum -y install python-twisted-core --nogpgcheck

# Setup ssh keys
RUN mkdir /home/mpiuser/.ssh
COPY ./mpiuser.pub /home/mpiuser/.ssh/authorized_keys
RUN chown -R mpiuser /home/mpiuser/.ssh

# Intall git
RUN yum clean all
RUN yum -y install git