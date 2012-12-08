cd `dirname $0`
user=`whoami`
sed -i 's#steam-login#steam-login-hacked#g' steam-login/DEBIAN/control
mkdir -p steam-login/etc
> steam-login/etc/steam-hacked
sudo chown -R root:root .
sudo dpkg --build steam-login .
sudo chown -R $user:$user .
rm -r steam-login/etc
sed -i 's#steam-login-hacked#steam-login#g' steam-login/DEBIAN/control

