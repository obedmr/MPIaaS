FROM bltavares/arch-ssh
MAINTAINER obed.n.munoz@gmail.com

# Add MPI user
RUN useradd mpiuser
RUN echo -e "secure\nsecure" | passwd mpiuser
RUN mkdir /home/mpiuser ; chown mpiuser.mpiuser /home/mpiuser

# Install Custom Software
RUN pacman-key --refresh-keys
RUN pacman -Syu --noconfirm  wget python rsync
RUN pacman-db-upgrade
RUN wget http://share.obedmr.com/archlinux/sowing-1.1.17-1-any.pkg.tar.xz
RUN pacman -U --noconfirm sowing-1.1.17-1-any.pkg.tar.xz
RUN wget http://share.obedmr.com/archlinux/mpich-3.1.4-1-x86_64.pkg.tar.xz
RUN pacman -U --noconfirm mpich-3.1.4-1-x86_64.pkg.tar.xz
RUN rm *.pkg.tar.xz
RUN echo "export PATH=$PATH:/opt/mpich/bin" >> /etc/profile

# Install python2 and twisted
RUN pacman -Sy --noconfirm python2 python2-twisted

# Setup ssh keys
RUN mkdir /home/mpiuser/.ssh
COPY ./mpiuser.pub /home/mpiuser/.ssh/authorized_keys
RUN chown -R mpiuser /home/mpiuser/.ssh

# Install git
RUN pacman -Sy --noconfirm git