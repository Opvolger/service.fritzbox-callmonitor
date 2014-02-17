'''
    FritzBox! Callmonitor
    ~~~~~~~~~~~~~~~~~~~~~

    Made by Bas Magre (Opvolger)
    
'''
from xbmcswift2 import Plugin
import xbmc, xbmcaddon
import os, time, errno
import socket, select

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
__language__    = __addon__.getLocalizedString

ip = __addon__.getSetting( "ip" )
displaytime = __addon__.getSetting( "displaytime" )
pauseplaying = __addon__.getSetting( "pauseplaying" )

displaytimeint = float(displaytime) * int(1000) # mini-sec to sec

xbmc.log("Start Fritzbox Callmonitor on "+ip+":1012")

input = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    input.connect((ip, 1012))
    while (not xbmc.abortRequested):    
        inputready,outputready,exceptready = select.select([input],[],[],2) # time out, without it a crash on exit XBMC
        for readsocket in inputready:
            data = readsocket.recv( 1024 )
            dataitems = data.split(';')
            if dataitems[1] == 'RING':
                xbmc.log('FritzBox!-RING: ' + data) # 14.02.14 23:52:56;RING;0;0612345678;0267894561;SIP0;                
                info = __language__(32101)%(dataitems[3])
                if (pauseplaying == 'true'):
                    player = xbmc.Player()
                    if player.isPlaying():
                        timenow = player.getTime()
                        xbmc.sleep(1000)
                        #do not onpause if the movie was all ready on pause.
                        if (timenow != player.getTime()):
                            player.pause()
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,info, displaytimeint, __icon__))
            elif dataitems[1] == 'CALL':
                #xbmc.log('FritzBox!-CALL: ' + data) # 14.02.14 23:54:40;CALL;0;1;0267894561;0612345678;SIP0;
                info = __language__(32102)%(dataitems[5])
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,info, displaytimeint, __icon__))
            elif dataitems[1] == 'CONNECT':
                #xbmc.log('FritzBox!-CONNECT: ' + data) # 15.02.14 00:34:14;CONNECT;0;1;0612345678;
                info = __language__(32103)%(dataitems[4])
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,info, displaytimeint, __icon__))
            elif dataitems[1] == 'DISCONNECT':
                #xbmc.log('FritzBox!-DISCONNECT: ' + data) # 15.02.14 00:34:27;DISCONNECT;0;13;
                info = __language__(32104)%(int(int(dataitems[3])/60))
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,info, displaytimeint, __icon__))
            else:
                xbmc.log('FritzBox!-' + dataitems[1] + ' unknown function!:' + data)
    input.close()
except socket.error, msg:
    text = 'ERROR: Could not connect open socket to: %s:1012'%(ip)
    xbmc.log(text)
finally:
    input.close()
input.close()
xbmc.log('Stop Fritzbox Callmonitor on %s:1012'%(ip))
