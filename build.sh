#!/bin/sh
cd `dirname $0`/steam-login
fakeroot dpkg-buildpackage -b -us -uc
dh_clean
