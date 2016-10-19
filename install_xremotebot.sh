#/bin/bash
WORKDIR=`dirname "$BASH_SOURCE"`
apt-get update

# General development essentials
apt-get install -y build-essential ssh git gitk

# Sqlite
apt-get install -y sqlite

# Python development essentials
apt-get install -y python python-setuptools python-dev && sudo easy_install -U pip
apt-get install -y libxml2-dev libxslt-dev  # needed for Python package 'lxml'

# virtualenv, virtualenvwrapper stuff
pip install virtualenv virtualenvwrapper
echo "
if [ -f /usr/local/bin/virtualenvwrapper.sh ] ; then
  . /usr/local/bin/virtualenvwrapper.sh
fi
export WORKON_HOME=~/Envs
" >> $HOME/.bashrc
PS1='$ '
source $HOME/.bashrc
mkdir -p $WORKON_HOME

# Add personal bin to path
echo '
# Add personal bin to PATH
if [ -d "$HOME/bin" ]; then
  PATH="$HOME/bin:$PATH"
fi
' >> $HOME/.bashrc

## XRemoteBot
git clone https://github.com/fernandolopez/xremotebot.git xremotebot
cd xremotebot
virtualenv $PWD
echo $PWD
source bin/activate
pip install -r requirements.txt
pip install git+https://github.com/Robots-Linti/duinobot.git
pip install git+https://github.com/fernandolopez/Myro.git
#streaming
add-apt-repository ppa:mc3man/trusty-media
apt-get update
apt-get dist-upgrade
apt-get install ffmpeg

