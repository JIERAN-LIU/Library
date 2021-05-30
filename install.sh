# install dependencies needed by python3.7
apt-get install build-essential checkinstall
apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev zlib1g-dev \
  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev

# get python source
cd /usr/local/

wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
tar -zxf Python-3.7.9.tgz
rm Python-3.7.9.tgz
cd Python-3.7.9
./configure --prefix=/usr/local/Python-3.7.9
make
make install

ln -s /usr/local/Python-3.7.9/bin/python3 /usr/bin/python3
ln -s /usr/local/Python-3.7.9/bin/python3 /usr/bin/python
ln -s /usr/local/Python-3.7.9/bin/pip3 /usr/local/bin/pip3
ln -s /usr/local/Python-3.7.9/bin/pip3 /usr/local/bin/pip

pip install uwsgi
ln -s /usr/local/Python-3.7.9/bin/uwsgi /usr/bin/uwsgi


# update openssl
cd /home/tiger
wget http://www.openssl.org/source/openssl-1.1.1.tar.gz
tar -zxvf openssl-1.1.1.tar.gz
cd openssl-1.1.1
./config --prefix=/home/tiger/openssl shared zlib
make && make install

# update env
vim /home/tiger/.bash_profile
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/tiger/openssl/lib
source /home/tiger/.bash_profile

# replace old openssl
mv /usr/bin/openssl /usr/bin/openssl.bak
mv /usr/include/openssl /usr/include/openssl.bak
ln -s /home/tiger/openssl/bin/openssl /usr/bin/openssl
ln -s /home/tiger/openssl/include/openssl /usr/include/openssl

cd /etc/ld.so.conf.d/

vim openssl-1.1.1.conf

/home/tiger/openssl/lib

ldconfig -v

openssl version

export LDFLAGS="-L/home/tiger/openssl/lib"
export CPPFLAGS="-I/home/tiger/openssl/include"
export PKG_CONFIG_PATH="/home/tiger/openssl/lib/pkgconfig"


