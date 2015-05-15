Some of these are trivial, here for reference, some are more involved.  They help me, hopefully they will help you.

## apachectl.py ##

A cute little icon to enable/disable apache and database (mysql/postgres).

I disable those from init startup like this:

```
sudo update-rc.d -f apache2 remove
sudo update-rc.d -f mysql remove
sudo update-rc.d -f postgresql-8.3 remove
```

Then I add apachectl.py to my xubuntu startup programs.

This makes it so I can just start it when I need it, with a simple little icon.

## volume\_control.py ##
A fancy volume control (like gnome) for non-gnome WMs.

use it like this:
assign multimedia keys (mute/volume up/volume down) to these actions:

```
volume_control.py mute
volume_control.py up
volume_control.py down
```

Add it to your win manager's  key-bindings, and you will have a cool little volume widget.

