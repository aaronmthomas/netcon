<h1>Netcon</h1>
It is under construction. 
Netcon is a graphic user interface program that allows a real time view of your network connections. It is created for Linux OS and you need python 2.7 version and wx library to run the program.

<br><br><p align="center">
<img src="https://github.com/ftsiadimos/netcon/blob/master/icons/image1.png" width="400" height="270" alt="Logo"/>
<img src="https://github.com/ftsiadimos/netcon/blob/master/icons/image2.png" width="400" height="270" alt="Logo"/>
<img src="https://github.com/ftsiadimos/netcon/blob/master/icons/image3.png" width="400" height="270" alt="Logo"/></p>

For Fedora 21 or 22 version you need to create the polkit rule to run the applicatation with the "run.py" script.


Copy the below script in this locatation "/usr/share/polkit-1/actions/netcon.policy"

``` vim  /usr/share/polkit-1/actions/netcon.policy```
------------------------------------------------------------------
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">

<policyconfig>
<vendor>Netcon</vendor>
<vendor_url>https://wiki.gnome.org/Apps/Netcon</vendor_url>
<action id="netcon">
<message>Authentication is required to run the Netcon</message>
<icon_name>netcon</icon_name>
<annotate key="org.freedesktop.policykit.exec.path">/home/fotis/bin/netcon.py</annotate>
<annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
<defaults>
 <allow_any>no</allow_any>
 <allow_inactive>auth_admin</allow_inactive>
 <allow_active>auth_admin</allow_active>
</defaults>
</action>

</policyconfig>
------------------------------------------------------------------


You need to install the wxPython library and the fail2ban service.

``` yum install wxPython
  yum install fail2ban
 systemctl start fail2ban ```
