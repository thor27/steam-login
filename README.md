steam-login
===========

Put STEAM BigPicture mode at login screen

NEWS
----

* Version 3
Improved multimonitor setup, loading gnome (unity) settings, chagend openbox to xfwm4: improving compatibility, removing unecessary new options added to login screen and fixing the need to "alt+tab" after playing a game in hacked version

* Version 2
Now use openbox Window Manager to improve game compatibility corectly setting focus on the active window. The openbox is now set as dependecy on the platform

KNOWN ISSUES
------------

Hacked version: After exiting you will need to press on the steam window on "steam" and after "exit". If you press in the close button the window will only minimize, you may need to press alt+tab again to gain focus and then exit it.

INSTALL
-------

Install <a href="https://github.com/downloads/thor27/steam-login/steam-login_3_all.deb">steam-login_3_all.deb</a> if you have access to the beta. This will still work if you don't access the beta, you just can't click on the window saying that the closed beta for mac (?!) is not available to you.

Install <a href="https://github.com/downloads/thor27/steam-login/steam-login-hacked_3_all.deb">steam-login-hacked_3_all.deb</a> if you do not have access to the beta. After exiting the big screen mode, you need to click on steam menu, and exit do quit. The close button won't work

HACKING ON IT
-------------
It's a pretty simple project.

You just need to put the correct files on steam-login or stea-login-hacked folder, as if was your / folder. on DEBIAN control you may change version dependencies and stuff

To build the package you just need to type:

```
dpkg --build steam-login .
```
where steam-login is the steam-login folder (ex: steam-login or steam-login hacked) and . is where the package should be.
Please fork-it and improve it :)
