steam-login
===========

Put STEAM BigPicture mode at login screen

NEWS
----
* *Version 7* <br/>
Code cleanup, fix bug while bigpicture was not working with newer steam versions, make it less intensive and changed Steam name to not be all caps anymore (thanks to Zeroedout <alishams.hassam@gmail.com>)

* *Version 6.1* <br/>
Change recommends to suggests for xserver-xorg-input-joystick as users may have trouble in some systems and other desktops

* *Version 6* <br/>
Shows error message when steam fails to run, add possibility to login with the gamepad in lightdm (Thanks to  pmk1c <ruben.uwe.grimm@gmail.com>), code cleanup, removed some useless workaround, thanks to steam fixes, replaced steam-de default folder

* *Version 5* <br/>
Added STEAM badge icon for lightdm, fixed bad quality package and improved package information, script modified to monitor windows, so steam always recover focus after gameplay and there is no need anymore to click in ok to close steam on non-hacked version

* *Version 4* <br/>
Improved compatibility with more games, support for nvidia optimus (if bumblebee and/or Primus is present), restart steam if it crashes, hack to close steam when not using the "hacked version", workaround for TF2 black screen bug and for text fonts bug with some specific fonts settings. 

* *Version 3* <br/>
Improved multimonitor setup, loading gnome (unity) settings, chagend openbox to xfwm4: improving compatibility, removing unecessary new options added to login screen and fixing the need to "alt+tab" after playing a game in hacked version

* *Version 2* <br/>
Now use openbox Window Manager to improve game compatibility corectly setting focus on the active window. The openbox is now set as dependecy on the platform

KNOWN ISSUES
------------

Steam, sometimes, may "hide" itself, mostly when something went wrong with a game or staem itself. If this happens just press ALT+TAB to get back do Steam Big Picture.


INSTALL
-------
To install, just add the ppa so you can keep track of package updates:

```
sudo add-apt-repository ppa:thor27-gmail/steam-desktop 
sudo apt-get update 
sudo apt-get install steam-login
```

If you don't (or can't) use PPA, you can directly donwload the latest version from here:
<a href="https://launchpad.net/~thor27-gmail/+archive/steam-desktop/+files/steam-login_7_all.deb">steam-login_7_all.deb</a>

HACKING ON IT
-------------
It's a pretty simple project.

You just need to put the correct files on steam-login or stea-login-hacked folder, as if was your / folder. on DEBIAN control you may change version dependencies and stuff

To build the package you just need to run the build.sh script:

```
./build.sh
```

Please fork-it and improve it :)
