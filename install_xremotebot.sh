#/bin/bash
set -e
apt-get update

# General development essentials
apt-get install -y build-essential git

# Sqlite
apt-get install -y sqlite

# Python development essentials
apt-get install -y python python-setuptools python-dev
apt-get install -y python-pip
apt-get install -y libxml2-dev libxslt-dev  # needed for Python package 'lxml'

# virtualenv
pip install virtualenv

## XRemoteBot
virtualenv $PWD
echo $PWD
source bin/activate
pip install -r requirements.txt
pip install git+https://github.com/Robots-Linti/duinobot.git
#pip install git+https://github.com/fernandolopez/Myro.git
#streaming
apt-get -y install ffmpeg

