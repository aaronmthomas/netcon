#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Fotios Tsiadimos
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
#sys.path.append('lib')
try:
    import wx
except:
    sys.exit("\nYou need to install the wx library.\n")
from taskbar import MyTaskBarIcon
from mainpanel import Main_Class
from networkpanel import Network_Class
from fail2ban import Logs_Class
if not os.geteuid()==0:
    sys.exit("\nOnly root can run this program. --> sudo python netcon.py <--\n")
class Mainpy(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,  style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER |wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN, size=(650,550))

        icon1 = wx.Icon("icons/netcon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        
        # Creating the Menubar
        ####################################################################
        menuBar = wx.MenuBar()
        filemenu= wx.Menu()
        viewMenu = wx.Menu()
        aboutmenu = wx.Menu()
        
        self.shst = viewMenu.Append(wx.ID_ANY, 'Hide frame on close', 
            'Hide frame on close', kind=wx.ITEM_CHECK)
            
        viewMenu.Check(self.shst.GetId(), True)
        
        self.Bind(wx.EVT_MENU, self.OnClose, self.shst)
           
        
        menuAbout = aboutmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(viewMenu, '&View')        
        menuBar.Append(aboutmenu, '&Help') 
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        ####################################################################        
        # Ending the Menubar


        # Creating the Toolbar
        ####################################################################
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT)
        toolbar.AddLabelTool(1, "Status", wx.Bitmap("icons/Home.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Home", "")
        toolbar.AddSeparator()        
        toolbar.AddLabelTool(2, "Networking", wx.Bitmap("icons/net.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Netwotking", "")
        toolbar.AddLabelTool(3, "Fail2ban", wx.Bitmap("icons/2.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Fail2ban", "")  
        toolbar.AddSeparator() 
        toolbar.AddLabelTool(7, "Exit", wx.Bitmap("icons/stop.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "Exit", "")
        toolbar.Realize()
        vbox.Add(toolbar, 0, wx.EXPAND)
       
        self.Bind(wx.EVT_TOOL, self.OnHome, id=1)
        self.Bind(wx.EVT_TOOL, self.OnNet, id=2)
        self.Bind(wx.EVT_TOOL, self.OnLogs, id=3)
        self.Bind(wx.EVT_TOOL, self.OnExit, id=7)
        ####################################################################        
        #Ending Toolbar        
        
           
        self.tskic = MyTaskBarIcon(self)  #Calling the taskbar
        self.Bind(wx.EVT_CLOSE, self.OnClose) #Closing button on window
        
       
        self.panel0 = Main_Class(self)       
        vbox.Add(self.panel0, -1, wx.EXPAND)

        self.panel1 = Network_Class(self)       
        vbox.Add(self.panel1, -1, wx.EXPAND)
        
        
        self.panel2 = Logs_Class(self)       
        vbox.Add(self.panel2, -1, wx.EXPAND)        

        
        self.SetSizer(vbox)
        self.Centre()
        self.panel0.showyourself()
               
    def OnHome(self, event):
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel0.showyourself()    

    def OnNet(self, event):
        self.panel0.Hide()
        self.panel2.Hide()
        self.panel1.showyourself()

    def OnLogs(self, event):
        self.panel1.Hide()
        self.panel0.Hide()
        self.panel2.showyourself()
    
    def OnClose(self, event):
        if not self.shst.IsChecked():
            self.Bind(wx.EVT_CLOSE, self.OnExit)
        else:
            self.Hide()
        
    def OnExit(self, event):
        self.Destroy()
        self.tskic.Destroy()
        
    def OnAbout(self,event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Netcon is a graphical tool to monitor\n your system\n Version: 1.00", "About Netcon", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.


class MyApp(wx.App):
    def OnInit(self):
        frame = Mainpy(None, -1, 'Netcon')
        frame.Show(True)
	frame.Center()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
