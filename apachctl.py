#!/usr/bin/env python

# very simple frontend for LAMP control

# on ubuntu, to install what you need:
# sudo apt-get install apache2
# for mysql : sudo apt-get install mysql-server phpmyadmin
# for postgres: sudo apt-get install postgresql-8.3 pgadmin3
# sudo chown -R `whoami` /var/www

import gtk
import pygtk

from subprocess import *
from os.path import exists

# SETTINGS

WEBROOT='/var/www'

# check if daemon script exists, turn off things, if it's not installed
USING_POSTGRES=exists('/etc/init.d/postgresql-8.3')
USING_MYSQL=exists('/etc/init.d/mysql')

# you could also do this:
# USING_POSTGRES=False
# USING_MYSQL=True


##############

def quit_cb(widget, data = None):
    if data:
        data.set_property('visible', False)
    gtk.main_quit()

def popup_menu_cb(widget, button, time, data = None):
    if button == 3:
        if data:
            data.show_all()
            update_toggles()
            data.popup(None, None, None, 3, time)

def get_status(name):
	pid = Popen(["pidof", name], stdout=PIPE).communicate()[0]
	if pid != '':
		return True
	else:
		return False


def toggle_apache(widget, data = None):
	if get_status('apache2'):
		p = Popen(['gksudo', '/etc/init.d/apache2', 'stop'])
	else:
		p = Popen(['gksudo', '/etc/init.d/apache2', 'start'])

def toggle_mysql(widget, data = None):
	if get_status('mysqld'):
		p = Popen(['gksudo', '/etc/init.d/mysql', 'stop'])
	else:
		p = Popen(['gksudo', '/etc/init.d/mysql', 'start'])


def toggle_pgsql(widget, data = None):
	if get_status('postgres'):
		p = Popen(['gksudo', '/etc/init.d/postgresql-8.3', 'stop'])
	else:
		p = Popen(['gksudo', '/etc/init.d/postgresql-8.3', 'start'])

def pgadmin(widget, data = None):
	p = Popen(['pgadmin3'])

def phpmyadmin(widget, data = None):
	p = Popen(['sensible-browser', 'http://localhost/phpmyadmin'])

def openroot(widget, data = None):
	p = Popen(['nautilus', '--no-desktop', WEBROOT])

def browsesite(widget, data = None):
	p = Popen(['sensible-browser', 'http://localhost'])


def update_toggles():
	# hide/show things based on what is running and what is installed
	if (get_status('apache2')):
		menuItemOpen.set_property('visible', True)
		menuItemBrowse.set_property('visible', True)
		if USING_MYSQL:
			menuItemPhpmyadmin.set_property('visible', get_status('mysqld'))
	else:
		menuItemOpen.set_property('visible', False)
		menuItemBrowse.set_property('visible', False)
		if USING_MYSQL:
			menuItemPhpmyadmin.set_property('visible', False)
	
	if USING_POSTGRES:
		if get_status('postgres'):
			menuItemPgadmin.set_property('visible', True)
		else:
			menuItemPgadmin.set_property('visible', False)
	

statusIcon = gtk.StatusIcon()
menu = gtk.Menu()

# setup menu, check current status to get started
menuItemToggleApache = gtk.CheckMenuItem("Apache")
menuItemToggleApache.set_active(get_status('apache2'))
menuItemToggleApache.connect('activate', toggle_apache, statusIcon)
menu.append(menuItemToggleApache)

if USING_MYSQL:
	menuItemToggleMysql = gtk.CheckMenuItem("Mysql")
	menuItemToggleMysql.set_active(get_status('mysqld'))
	menuItemToggleMysql.connect('activate', toggle_mysql, statusIcon)
	menu.append(menuItemToggleMysql)

if USING_POSTGRES:
	menuItemTogglePgsql = gtk.CheckMenuItem("Postgres")
	menuItemTogglePgsql.set_active(get_status('postgres'))
	menuItemTogglePgsql.connect('activate', toggle_pgsql, statusIcon)
	menu.append(menuItemTogglePgsql)

menuItemBrowse = gtk.MenuItem("Browse Site Page")
menuItemBrowse.connect('activate', browsesite, statusIcon)
menu.append(menuItemBrowse)

menuItemOpen = gtk.MenuItem("Open Site Dir")
menuItemOpen.connect('activate', openroot, statusIcon)
menu.append(menuItemOpen)

if USING_MYSQL:
	menuItemPhpmyadmin = gtk.MenuItem("Admin Mysql")
	menuItemPhpmyadmin.connect('activate', phpmyadmin, statusIcon)
	menu.append(menuItemPhpmyadmin)

if USING_POSTGRES:
	menuItemPgadmin = gtk.MenuItem("Admin Postgres")
	menuItemPgadmin.connect('activate', pgadmin, statusIcon)
	menu.append(menuItemPgadmin)

menuItemQuit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
menuItemQuit.connect('activate', quit_cb, statusIcon)
menu.append(menuItemQuit)

statusIcon.set_from_stock(gtk.STOCK_HOME)
statusIcon.set_tooltip("Developer System Controller")
statusIcon.connect('popup-menu', popup_menu_cb, menu)
statusIcon.set_property('visible', True)

gtk.main()
