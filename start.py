#! /usr/bin/python3

from wgadget.wg_light import WGLight

if __name__ == "__main__":

    wgLight = WGLight()

    try:
        wgLight.run(host= '0.0.0.0', debug=False)
#        wgLight.run()

    finally:
        wgLight.unconfigure()
