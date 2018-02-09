#   plugin.service.rawmaintenance, Raw Media's XBMC Maintenance Tool Startup Process
#   Copyright (C) 2014  Adam Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import xbmc, xbmcgui, xbmcaddon
import os, sys, statvfs, time, datetime
from time import mktime
import feedparser
 
__addon__       = xbmcaddon.Addon(id='plugin.service.rawmaintenance')
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.service.rawmaintenance')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')


#######################################################################
#							RSS
#######################################################################
global rss
global lastCheck

def rssStartup():
    global rss
    global lastCheck 

    string = ''

    print "----####RSS STARTUP####----"
    rss = feedparser.parse('http://notanrss.info/rss.vex')
    if rss.bozo:
        return
    
    try:
        fo = open(os.path.join(addonPath, "lastAccess.bin"), "rb+")
    except:
        #if file doesn't exist create a new one
        fo = open(os.path.join(addonPath, "lastAccess.bin"), "wb+")
        fo.write(time.strftime('%m/%d/%Y %I:%M:%S %p', (1993, 1, 1, 1,1,1,1,1,1)))
    fo.seek(0)
    string = fo.readline()
    fo.seek(0)
    fo.write(time.strftime('%m/%d/%Y %I:%M:%S %p'))
    fo.close()
    
    print "LAST CHECKED DATE: "+ string
    lastCheck = time.strptime(string, '%m/%d/%Y %I:%M:%S %p')
    
    checkStories()

def checkStories():
    global rss
    global lastCheck
    
    for story in rss.entries:
        publish = time.strptime(story.published[:-6], '%a, %d %b %Y %H:%M:%S')
        publishd = datetime.datetime.fromtimestamp(mktime(publish))
        if abs((publishd - datetime.datetime.now()).days) < 14 and publish > lastCheck:
            rssShowStory(story)

def rssShowStory(story):
    global rss

    dialog = xbmcgui.Dialog()
    dialog.ok(story.title, story.description)

#######################################################################
#							MAIN
#######################################################################

if __name__ == '__main__':
    #check HDD freespace
    try:
        st = os.statvfs(xbmc.translatePath('special://home'))
    except:
        print "Statvfs error.  Currently in development."
        while not xbmc.abortRequested:    
            xbmc.sleep(500)
    
    if st.f_frsize:
        freespace = st.f_frsize * st.f_bavail/1024/1024
    else:
        freespace = st.f_bsize * st.f_bavail/1024/1024
    
    print "Free Space: %dMB"%(freespace)
    if(freespace < 500):
        text = "You have less than 500MB of free space"
        text1 = "Please use the Raw Maintenance tool"
        text2 = "immediately to prevent system issues"

        xbmcgui.Dialog().ok(__addonname__, text, text1, text2)

    #rss check
    rssStartup()

    while not xbmc.abortRequested:    
        xbmc.sleep(500)
