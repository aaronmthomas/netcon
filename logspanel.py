#!/usr/bin/env python
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

import wx
import sys
import socket
import re
from ConfigParser import SafeConfigParser



FILE_PATH = '/var/log/fail2ban.log'

class Logs_Class(wx.Panel):
    """Show  connections which firewall has stopped"""
    def __init__(self, parent, idwx= -1):

        wx.Panel.__init__(self, parent, idwx)

        mastersizer = wx.BoxSizer(wx.VERTICAL)
        mastersizer.AddSpacer(15)
        #tee = wx.StaticText(self, -1, 'TEST')
	box = wx.CheckBox(self, label='Enable Fail2ban')
	box.Bind(wx.EVT_CHECKBOX, self.ShowOrHideTitle)
	box.SetValue(True)

        distros = ['ssh', 'apache', 'mail', 'webmin']
	cb = wx.ComboBox(self, choices=distros, 
			            style=wx.CB_READONLY)
	self.st = wx.StaticText(self, label='')
	cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)


        txtheader = wx.StaticText(self, -1, 'Fail2ban', (0, 0))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        txtheader.SetFont(font)
               
        rowtopsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowtopsizer.Add(txtheader, 3, wx.ALIGN_LEFT) 
        rowtopsizer.Add((0, 0), 1)  
      
        mastersizer.Add(rowtopsizer, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15) 
        
	sizerv = wx.BoxSizer(wx.HORIZONTAL) 
        #sizerv.Add(tee, 1, wx.ALIGN_LEFT)
	sizerv.Add(box, 1, wx.ALIGN_LEFT)
        sizerv.Add(cb, 1, wx.ALIGN_RIGHT)
	sizerv.Add(self.st, 1, wx.ALIGN_RIGHT)
	#sizerv.Add(self.ff, 1, wx.ALIGN_RIGHT)


        mastersizer.Add(sizerv, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        self.tab1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_VRULES |wx.EXPAND)

        self.tab1.InsertColumn(0, 'Time', width=120)
        self.tab1.InsertColumn(1, 'Port', width=100)
        self.tab1.InsertColumn(2, 'Source', width=140)
        self.tab1.InsertColumn(3, 'Protocol', width=100)
        self.tab1.InsertColumn(4, 'Service', width=180)

        mastersizer.Add(self.tab1, 1, wx.EXPAND)        
        
        wx.EVT_TIMER(self, -1, self._ontimer)

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        
        rowbottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        mastersizer.Add(rowbottomsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        mastersizer.AddSpacer(15)   
        self.SetSizer(mastersizer)
        self.cur_view = []
        self.Hide()


    def ShowOrHideTitle(self, e):
        parser = SafeConfigParser()
        parser.read('/home/fotis/bin/text.txt')


        sender = e.GetEventObject()
        isChecked = sender.GetValue()

        if isChecked:
            parser.set('sshd','port','yes')
            #self.SetTitle('wx.CheckBox')
            #self.st1.SetLabel(parser.get('sshd', 'port'))

        else:
            parser.set('sshd','port','no')
            #self.SetTitle('')
            #self.st1.SetLabel(parser.get('sshd', 'port'))
        with open('/home/fotis/bin/text.txt', 'wb') as configfile:
            parser.write(configfile)





    def OnSelect(self, e):
        t = e.GetString()
	self.st.SetLabel(t)
	#self.ff = wx.CheckBox(self, label='Enable:'+t)
	#sizerv.Add(ff, 1, wx.ALIGN_RIGHT)
    def _openfile(self):
         try:
            lis = ['NOTICE']
            self.cc= []
            items = open(FILE_PATH)
            for item in items:
                if  'NOTICE' in item:
                        aa = item.split()
                        self.cc.append(aa)
            items.close()
	   # print self.cc
            return self.cc
         except IOError:
            print ("You need to activate the log file messages in your /var/log folder.")
	    sys.exit()  
    def _ontimer(self, event):
        """Refresh log messages."""
        aa = self._openfile()
        for i in aa:
            a = str(i[4])
            b = str(i[5])
            c = str(i[6])
            d = str(i[7])
            #try:
             #   service = socket.getservbyport(int(d))
            #except:
             #   service = 'Unknown'
             
            if i not in self.cur_view:
                    index = self.tab1.InsertStringItem(sys.maxint, a)
                    self.tab1.SetStringItem(index, 1, b)
                    self.tab1.SetStringItem(index, 2, d)
                    self.tab1.SetStringItem(index, 3, c)
                    #self.tab1.SetStringItem(index, 4, a)
                    self.cur_view.append(i)
                        
            count_rows = self.tab1.GetItemCount()
            for row in range(count_rows):
                if row % 2:
                    self.tab1.SetItemBackgroundColour(row, "#FFFFFF")
                else:
                    self.tab1.SetItemBackgroundColour(row, "#E5E5E5")
                    self.tab1.SetBackgroundStyle(wx.LC_HRULES)

        
    def showyourself(self):
        """Shows the panel on the main frame."""
        self.Raise()
        self.SetPosition((0, 0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)
        self.GetParent().GetSizer().Layout()
       
        
if __name__ == "__main__":
    print "This is a module for netcon.py"
