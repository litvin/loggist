#!/bin/bash
#sudo yum install zlib-devel bzip2-devel
#sudo yum install xz gcc

wget https://www.python.org/ftp/python/3.3.6/Python-3.3.6.tar.xz
unxz ./Python-3.3.6.tar.xz 
tar xvf ./Python-3.3.6.tar
cd ./Python-3.3.6
./configure 
make
sudo  make install
sudo ln -s /usr/local/bin/python3.3 /usr/bin/python3.3
cd ../

wget http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip
unzip  ./mysql-connector-python-2.0.4.zip -d ./
cd ./mysql-connector-python-2.0.4
sudo python3 setup.py install
cd ../

sudo cp ./log.py /root/scripts/log.py
sudo chmod +x /root/scripts/log.py
