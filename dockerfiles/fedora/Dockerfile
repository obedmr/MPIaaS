FROM fedora
MAINTAINER obed.n.munoz@gmail.com

# Update 
RUN yum -y update --nogpgcheck
RUN yum -y clean all

# Install and configure custom software
RUN yum -y install mpich --nogpgcheck && yum clean all