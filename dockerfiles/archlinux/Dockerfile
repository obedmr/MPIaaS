FROM base/archlinux
MAINTAINER obed.n.munoz@gmail.com

# Install ArchLinux Development Tools
RUN pacman-key --refresh-keys
RUN pacman -Syu --noconfirm --needed base-devel wget python
RUN useradd -G wheel builder || true
RUN echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
COPY yaourt.repo /tmp/
RUN cat /tmp/yaourt.repo >> /etc/pacman.conf

# Install and configure custom software
RUN pacman-db-upgrade
RUN pacman -Syu --noconfirm yaourt
RUN su builder -c "yaourt -Sy --noconfirm mpich"
RUN rm -rf /var/cache/pacman/pkg/*
RUN pacman -Rsn --noconfirm base-devel