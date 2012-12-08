steam-login
===========

Put STEAM BigPicture mode at login screen

NEWS
----

*Version 5* <br/>
Added STEAM badge icon for lightdm, fixed bad quality package and improved package information, script modified to monitor windows, so steam always recover focus after gameplay and there is no need anymore to click in ok to close steam on non-hacked version

* *Version 4* <br/>
Improved compatibility with more games, support for nvidia optimus (if bumblebee and/or Primus is present), restart steam if it crashes, hack to close steam when not using the "hacked version", workaround for TF2 black screen bug and for text fonts bug with some specific fonts settings. 

* *Version 3* <br/>
Improved multimonitor setup, loading gnome (unity) settings, chagend openbox to xfwm4: improving compatibility, removing unecessary new options added to login screen and fixing the need to "alt+tab" after playing a game in hacked version

* *Version 2* <br/>
Now use openbox Window Manager to improve game compatibility corectly setting focus on the active window. The openbox is now set as dependecy on the platform

KNOWN ISSUES
------------

Hacked version: After exiting you will need to press on the steam window on "steam" and after "exit". If you press in the close button the window will only minimize, you may need to press alt+tab again to gain focus and then exit it.

INSTALL
-------

Install <a href="https://github.com/downloads/thor27/steam-login/steam-login_5_all.deb">steam-login_5_all.deb</a> if you have access to the beta. This will still work if you don't access the beta, you just can't click on the window saying that the closed beta is not available to you.

Install <a href="https://github.com/downloads/thor27/steam-login/steam-login-hacked_5_all.deb">steam-login-hacked_5_all.deb</a> if you do not have access to the beta. After exiting the big screen mode, you need to click on steam menu, and exit do quit. The close button won't work. NOT TESTED ON VERSION 5

HACKING ON IT
-------------
It's a pretty simple project.

You just need to put the correct files on steam-login or stea-login-hacked folder, as if was your / folder. on DEBIAN control you may change version dependencies and stuff

To build the package you just need to run the build.sh script:

```
./build.sh
```

Please fork-it and improve it :)
