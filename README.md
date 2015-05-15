# dkbits
Little code snippets that were useful for soemthing

## apachectl.py

Very simple frontend for LAMP control.

on Ubuntu, to install what you need:

* `sudo apt-get install apache2`
* for mysql : `sudo apt-get install mysql-server phpmyadmin`
* for postgres: `sudo apt-get install postgresql-8.3 pgadmin3`

To take ownership of webroot:

    sudo chown -R `whoami` /var/www

## volume_control.py
This is a pretty volume-control, like the gnome one.

I use it in xubuntu with compiz running, and it looks very nice.
I attach it to multimedia keys in `Settings/Keyboard/Application Shortcuts`

use it like this:

* `volume_control.py mute` - to toggle muting
* `volume_control.py up` - turn up volume
* `volume_control.py down` - turn down volume
* `volume_control.py CARDNUM mute` - use same as aabove, for a specific card
