sudo apt-get update

# General development essentials
sudo apt-get install -y build-essential ssh git gitk

# Sqlite
sudo apt-get install -y sqlite

# Python development essentials
sudo apt-get install -y python python-setuptools python-dev && sudo easy_install -U pip
sudo apt-get install -y libxml2-dev libxslt-dev  # needed for Python package 'lxml'

# virtualenv, virtualenvwrapper stuff
sudo pip install virtualenv virtualenvwrapper
echo "
if [ -f /usr/local/bin/virtualenvwrapper.sh ] ; then
  . /usr/local/bin/virtualenvwrapper.sh
fi
export WORKON_HOME=~/Envs
" >> $HOME/.bashrc
. $HOME/.bashrc
mkdir -p $WORKON_HOME

# Add personal bin to path
echo '
# Add personal bin to PATH
if [ -d "$HOME/bin" ]; then
  PATH="$HOME/bin:$PATH"
fi
' >> $HOME/.bashrc

## XRemoteBot
git clone https://github.com/fernandolopez/xremotebot.git
cd xremotebot
virtualenv .
. bin/activate
pip install -r requirements.txt
pip install git+https://github.com/Robots-Linti/duinobot.git
pip install git+https://github.com/fernandolopez/Myro.git
sudo apt-get install libav-tools nodejs 
npm install ws
