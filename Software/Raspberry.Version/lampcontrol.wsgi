#!/usr/bin/python3

import sys
sys.path.insert(0,"/var/www/FLASKAPPS/")

from lampcontrol.start import app as application


from wgadget.wg_light import WGLight
application = WGLight()

