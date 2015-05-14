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