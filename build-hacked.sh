
sed -i 's#steam-login#steam-login-hacked#g' steam-login/DEBIAN/control
mkdir -p steam-login/etc
> steam-login/etc/steam-hacked
dpkg --build steam-login .
rm -r steam-login/etc
sed -i 's#steam-login-hacked#steam-login#g' steam-login/DEBIAN/control

