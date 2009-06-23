#!/usr/bin/env python

# this is a pretty volume-control, like the gnome one
# I use it in xubuntu with compiz running.
# looks very nice.

# I attach it to multimedia keys in Settings/Keyboard/APplication Shortcuts

# use it like this:
# volume_control.py mute - to toggle muting
# volume_control.py up - turn up volume
# volume_control.py down - turn down volume
#
# or
# volume_control.py CARDNUM mute
# etc...


import sys
import pygtk
pygtk.require("2.0")
import gobject
import gtk
import cairo
from gtk import gdk
import rsvg
import os
import alsaaudio

from threading import Timer


# you can set this up however you want, should go from lowest to highest value:

icon_dir = "/usr/share/icons/Tango/scalable/status/"
vol_icons=(
	"audio-volume-muted.svg",
	"audio-volume-low.svg",
	"audio-volume-medium.svg",
	"audio-volume-high.svg",
)

# this is how much to raise/lower volume:
volume_increment = 10

# this is how long to show window, in seconds
timeout = 0.5

def expose(widget, event, svg):
	ctx = widget.window.cairo_create()
	
	# clear window
	ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
	ctx.set_operator(cairo.OPERATOR_SOURCE)
	ctx.paint()
	
	# scale SVG
	matrix = cairo.Matrix(4,0,0,4,0, 0)
	ctx.transform (matrix)
	svg.render_cairo(ctx)
	
	return True

def screen_changed(widget, old_screen = None):
	screen = widget.get_screen()
	colormap = screen.get_rgba_colormap()
	
	if colormap == None:
		print "Your screen does not support alpha"
		colormap = screen.get_rgb_colormap()
	
	widget.set_colormap(colormap)
	
	return True

def main(args):
	if (len(args) == 3):
		card=int(args[1])
		vol=args[2]
	else:
		card = 0
		vol=args[1]
	
	try:
		mixer = alsaaudio.Mixer("Master", cardindex=card)
	except alsaaudio.ALSAAudioError:
		sys.stderr.write("No such mixer\n")
		sys.exit(1)
	
	channel = alsaaudio.MIXER_CHANNEL_ALL
	
	if vol == "mute":
		if mixer.getmute()[0] == 0:
			vol = 0
			mixer.setmute(1, channel)
		else:
			vol = mixer.getvolume()[0]
			mixer.setmute(0, channel)
	else:
		if vol == "up":
			vol =  mixer.getvolume()[0] + volume_increment
		elif vol == "down":
			vol =  mixer.getvolume()[0] - volume_increment
		
		if vol > 100:
			vol = 100
		if vol < 0:
			vol = 0
		
		mixer.setvolume(int(vol), channel)
	
	print "Volume on card %d set to %d" % (card, vol)
	
	icon = vol_icons[int((float(vol)/100.00) * float(len(vol_icons)-1))]
	
	svg = rsvg.Handle(os.path.join(icon_dir, icon))
	
	win = gtk.Window()
	win.set_position(gtk.WIN_POS_CENTER)
	
	win.set_title("Volume Control")
	win.set_app_paintable(True)
	win.set_skip_pager_hint(True)
	win.set_skip_taskbar_hint(True)

	win.set_decorated(False)
	
	win.resize(svg.props.width*4, svg.props.height*4)
	win.set_keep_above(True)
	
	win.connect("delete-event", gtk.main_quit)
	win.connect("expose-event", expose, svg)
	win.connect("screen-changed", screen_changed)
	
	
	# this is just for debugging... clickable window
	# win.add_events(gdk.BUTTON_PRESS_MASK)
	# win.connect("button-press-event", gtk.main_quit)
	
	screen_changed(win)
	
	win.show_all()
	
	gdk.threads_init()
	Timer(timeout, gtk.main_quit).start()
	
	gtk.main()
	
	return True

if __name__ == '__main__':
	main(sys.argv)

