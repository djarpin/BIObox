#!/bin/bash

# Get dependencies for Python altinstall
sudo yum -y groupinstall "Development tools"
sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

# Python altinstall to prevent affecting yum
wget --no-check-certificate https://www.python.org/ftp/python/3.2.5/Python-3.2.5.tar.xz
tar xf Python-3.2.5.tar.xz
cd Python-3.2.5
./configure --prefix=/usr/local
make 
sudo make altinstall

# Install biogeme
cd ../
wget http://biogeme.epfl.ch/v23/biogeme-2.3.tar.gz
tar xzf biogeme-2.3.tar.gz
cd biogeme-2.3
./configure --enable-bison --enable-python --with-python-dir=/usr/local/bin/
make
sudo make install
