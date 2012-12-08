cd `dirname $0`
user=`whoami`
sudo chown -R root:root .
sudo dpkg --build steam-login .
sudo chown -R $user:$user .
