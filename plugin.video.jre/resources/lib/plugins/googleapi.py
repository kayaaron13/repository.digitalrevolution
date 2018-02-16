'''
    googleapi.py --- Jen Plugin for accessing YouTube data using the Google Api
    Copyright (C) 2017, SpezC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Please Visit https://developers.google.com/ for all documentation pertaining to this api and how to use it.
You must enable YouTube Data APIv3 and obtain your youtube api key as well as your google ref header.


This is the default googleapis URL.  This is set to eventType=completed&type=video&q=24/7 cartoons
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=24/7%20cartoon&regionCode={}&maxResults=50&key={}

with key entered example
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=24/7%20cartoon&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs

live mixed sports    
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=live&type=video&q=sports&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs    

boxing replays
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=boxing&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs

concert replays
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=concerts&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs

documentary
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=documentaries&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs

historical events
https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=historical%20events&regionCode=US&maxResults=50&key=AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs

    <dir>
		<title>24/7 Cartoons</title>
		<googleapitoons>cartoons</googleapitoons>
	</dir>
'''

import urlparse
import urllib
from urlparse import parse_qsl
from urllib import urlencode
import xbmcplugin
import HTMLParser
import xbmcaddon
import requests
import xbmcgui
import base64
import json
import xbmc
import sys
import __builtin__
import pickle
import time
import koding
import xbmc
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
fanart = xbmcaddon.Addon().getAddonInfo('fanart')
icon = xbmcaddon.Addon().getAddonInfo('icon')
addonname = xbmcaddon.Addon().getAddonInfo('name')
region = "US"
key = "AIzaSyCOMD3M2mFhIAspyuWfI_7X4NpTvB03qXs" # Your YouTube Key Goes Here
headers = {'Referer':"c3R2bWMubmV0"}			# Your YouTuve Referer Key Goes Here
blacklist = ['news','music','radio','nasa','chat']
regulate = HTMLParser.HTMLParser()

class GOOGLEAPITOONS(Plugin):
    name = "googleapitoons"
    
    def process_item(self, item_xml):
        if "<googleapitoons>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "googleapitoons",
                'url': item.get("googleapitoons", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

    
def get_url(**kwargs):
    kwargs = {k: unicode(v).encode('ascii', 'ignore') for k,v in kwargs.iteritems()}
    return '{0}?{1}'.format(_url, urlencode(kwargs))

@koding.route("googleapitoons")      
def STREAMS(link=None):
    if link is None:
        link = 'https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=24/7%20cartoon&regionCode={}&maxResults=50&key={}'.format(region, key)
    req = requests.get(link, headers=headers)
    if req.status_code == 200:
        res = json.loads(req.text)
        if not len(res['items']) == 0:
            for stream in res['items']:
                skip = False
                for word in blacklist:
                    if any(w in stream['snippet']['title'].lower() for w in [' '+word,word+' ']):
                        skip = True
                        break
                if skip: continue
                list_item = xbmcgui.ListItem(label=regulate.unescape(stream['snippet']['title'].encode("ascii", "ignore").encode('utf-8')))
                list_item.setArt({'fanart':fanart,'thumb':stream['snippet']['thumbnails']['high']['url']})
                list_item.setProperty('IsPlayable','true')
                l = 'plugin://plugin.video.youtube/play/?video_id=%s' % stream['id']['videoId']
                xbmcplugin.addDirectoryItem(_handle, l, list_item, False)
            next_page = res.get('nextPageToken')
            if next_page:
                list_item = xbmcgui.ListItem(label='[COLOR yellow]Next Page >>>[/COLOR]')
                call = 'https://www.googleapis.com/youtube/v3/search?part=snippet&eventType=completed&type=video&q=24/7%20cartoon&regionCode={}&maxResults=50&key={}'.format(region, key)
                url = get_url(mode='googleapitoonsnext', source='Googleapi',endpoint=call+'&pageToken='+next_page)
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(_handle)
    else:
        if req.status_code == 400 and 'unsupportedRegionCode' in req.text: 
            e = 'Stream unavailable in your region. Please change region code in settings and try again.'
        elif req.status_code == 429: 
            e = 'Too Many Requests, please wait a minute and try again.\nIf issue persists please add personal Youtube api key in settings.'
        elif req.status_code == 410:
            e = 'Stream has been taken down, please try another one.'
        elif req.status_code == 503: 
            e = 'Youtube Api is temporarily down, please try again in a bit.'
        else: 
            e = 'Unknown error occurred. Please try again later.'
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(addonname, e, 10000, icon))
        print req.text
        
@koding.route("googleapitoonsnext")
def router(paramstring = (sys.argv[2][1:])):
    params = dict(parse_qsl(paramstring))
    params.pop('source')
    link = params.get('endpoint')
    if params:
        if link: STREAMS(link)
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        STREAMS()
                  
if __name__ == '__main__':
    router(sys.argv[2][1:])
