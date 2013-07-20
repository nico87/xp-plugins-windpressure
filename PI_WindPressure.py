# -*- coding: utf-8 -*-
"""
Wind and Pressure plugin V1.0

This plugin shows the QNH and the current wind when you press F1.

This file is released under the GNU GPL v2 licence.

Author: Claudio Nicolotti - https://github.com/nico87/

If you want to update this plugin or create your own fork please visit https://github.com/nico87/xp-plugins-windpressure
"""

from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *

SHOW_TIMER = 5  # Show the window for this amount of seconds


class PythonInterface:
    """
    XPluginStart

    Our start routine registers our window and does any other initialization we
    must do.
    """
    def XPluginStart(self):
        """
        First we must fill in the passed in buffers to describe our
        plugin to the plugin-system."""
        self.Name = "WindPressure"
        self.Sig = "aimappy.xplane.PythonWindPressure"
        self.Desc = "A plugin that shows the current wind speed/direction and baro pressure."
        self.ShowWindow = False
        self.Counter = SHOW_TIMER
        self.WindDirDataRef = XPLMFindDataRef("sim/weather/wind_direction_degt")
        self.WindSpeedDataRef = XPLMFindDataRef("sim/weather/wind_speed_kt")
        self.QNHDataRef = XPLMFindDataRef("sim/weather/barometer_sealevel_inhg")
        """
        Now we create a window.  We pass in a rectangle in left, top,
        right, bottom screen coordinates.  We pass in three callbacks."""
        self.DrawWindowCB = self.DrawWindowCallback
        self.KeyCB = self.KeyCallback
        self.MouseClickCB = self.MouseClickCallback
        self.WindowId = XPLMCreateWindow(self, 50, 600, 250, 550, 1, self.DrawWindowCB, self.KeyCB, self.MouseClickCB, 0)
        self.FlightLoopCB = self.FlightLoopCallback
        XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 1.0, 0)
        self.MyHotKeyCB = self.MyHotKeyCallback
        self.HotKey = XPLMRegisterHotKey(self, XPLM_VK_F1, xplm_DownFlag, "Check weather", self.MyHotKeyCB, 0)
        return self.Name, self.Sig, self.Desc

    """
    XPluginStop

    Our cleanup routine deallocates our window.
    """
    def XPluginStop(self):
        # Unregister the callback
        XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)
        XPLMDestroyWindow(self, self.WindowId)
        pass

    """
    XPluginEnable.

    We don't do any enable-specific initialization, but we must return 1 to indicate
    that we may be enabled at this time.
    """
    def XPluginEnable(self):
        return 1

    """
    XPluginDisable

    We do not need to do anything when we are disabled, but we must provide the handler.
    """
    def XPluginDisable(self):
        pass

    """
    XPluginReceiveMessage

    We don't have to do anything in our receive message handler, but we must provide one.
    """
    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    """
    MyDrawingWindowCallback

    This callback does the work of drawing our window once per sim cycle each time
    it is needed.  It dynamically changes the text depending on the saved mouse
    status.  Note that we don't have to tell X-Plane to redraw us when our text
    changes; we are redrawn by the sim continuously.
    """
    def DrawWindowCallback(self, inWindowID, inRefcon):
        # First we get the location of the window passed in to us.
        lLeft = []
        lTop = []
        lRight = []
        lBottom = []
        windDir = 0
        windSpeed = 0
        QNH = 0
        XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
        left = int(lLeft[0])
        top = int(lTop[0])
        right = int(lRight[0])
        bottom = int(lBottom[0])

        if (self.ShowWindow is False):
            return

        windDir = XPLMGetDataf(self.WindDirDataRef)
        windSpeed = XPLMGetDataf(self.WindSpeedDataRef)
        QNH = XPLMGetDataf(self.QNHDataRef)

        """
        We now use an XPLMGraphics routine to draw a translucent dark
        rectangle that is our window's shape.
        """
        gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
        color = 1.0, 1.0, 1.0

        Desc = "Wind: %03d° %dkts" % (round(windDir), round(windSpeed))
        gResult = XPLMDrawString(color, left + 5, top - 20, Desc, 0, xplmFont_Basic)
        Desc = "QNH: %.2f InHg - %d mb" % (QNH, QNH * 33.8637526)
        gResult = XPLMDrawString(color, left + 5, top - 35, Desc, 0, xplmFont_Basic)
        pass

    """
    MyHandleKeyCallback

    Our key handling callback does nothing in this plugin.  This is ok;
    we simply don't use keyboard input.
    """
    def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
        pass

    """
    MyHandleMouseClickCallback

    Our mouse click callback toggles the status of our mouse variable
    as the mouse is clicked.  We then update our text on the next sim
    cycle.
    """
    def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        if (self.Counter > 0):
            self.Counter = self.Counter - 1
            if (self.Counter == 0):
                self.ShowWindow = False
        # Return 1.0 to indicate that we want to be called again in 1 second.
        return 1.0

    def MyHotKeyCallback(self, inRefcon):
        self.Counter = SHOW_TIMER
        self.ShowWindow = True
        pass
