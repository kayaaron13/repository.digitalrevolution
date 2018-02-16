"""
    midstock.py --- Youraddonname Plugin emulating the midstock addon
    Copyright (C) 2017, CandyLand

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
"""
import re
import sys

from BeautifulSoup import BeautifulSoup as BS

import koding
import xbmc
import xbmcaddon
import xbmcgui
from koding import route
from resources.lib.util.context import get_context_items
from resources.lib.util.url import replace_url
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

from ..plugin import Plugin

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
addon_name = xbmcaddon.Addon().getAddonInfo('name')


class MidStock(Plugin):
    name = "midstock"

    def process_item(self, item_xml):
        if "<midstock>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': replace_url(item.get("thumbnail", addon_icon)),
                'fanart': replace_url(item.get("fanart", addon_fanart)),
                'mode': "midstock",
                'url': item.get("midstock", ""),
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


@route(mode='midstock', args=["url"])
def midstock(url):
    if url == "main":
        xml = getmenu()
    elif url.startswith("play_channel"):
        play_url = url.replace("play_channel(", "")[:-1]
        play_channel(play_url)
        return
    else:
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(url)
        if not method:
            raise NotImplementedError("Method %s not implemented" % url)
        xml = method()
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def getmenu():
    xml = ""
    live_festivals = []
    vod_festivals = [("Pukkelpop", "pukkelvod", "", ""), (
        "Wacken", "wackenvod",
        "http://static.wacken.com/images/woa2017/top-headerlogo-livestream-2017.png",
        "http://static.wacken.com/images/woa2017/bg-body.jpg"
    ), (
        "Graspop", "graspopvod", "",
        "https://www.graspop.be/assets/default/images/src/vod_background.jpg"
    ), ("Rock Werchter", "werchtervod", "",
        "https://www.graspop.be/assets/default/images/src/vod_background.jpg")]
    for title, url, icon, fanart in live_festivals:
        label = "{} (Live)".format(title)
        xml += "<dir>" \
               "<title>%s</title>" \
               "<midstock>%s</midstock>"\
               "<thumbnail>%s</thumbnail>" \
               "<fanart>%s</fanart>" \
               "<summary>%s</summary>" \
               "</dir>" % (label, url, addon_icon, fanart, title)
    for title, url, icon, fanart in vod_festivals:
        label = "{} (VOD)".format(title)
        xml += "<dir>" \
               "<title>%s</title>" \
               "<midstock>%s</midstock>"\
               "<thumbnail>%s</thumbnail>" \
               "<fanart>%s</fanart>" \
               "<summary>%s</summary>" \
               "</dir>" % (label, url, addon_icon, fanart, title)
    return xml


def pukkelvod(url="http://vod.pukkelpop.be/"):
    xml = ""
    html = BS(koding.Open_URL(url + "/?language=en"))
    container = html.find("div", attrs={"id": "vod-list-container"})
    items = container.findAll("div", attrs={"class": re.compile("block .*")})
    for stream_li in items:
        stream_channel_link = stream_li.find("a")
        try:
            group = stream_li.find(
                "h3", attrs={"class": "block-content__title"}).text
            vodtype_type = stream_li.find(
                "span", attrs={"class": "block-content__subtitle"}).text
            group = group.replace(vodtype_type, "") +\
                " (%s)" % vodtype_type
            pic = stream_li.find("img")["src"]
        except:
            continue
        href = stream_channel_link["href"]
        xml_url = "play_channel({})".format("http://vod.pukkelpop.be/" + href)
        xml += "<item>" \
               "<title>%s</title>" \
               "<midstock>%s</midstock>"\
               "<thumbnail>%s</thumbnail>" \
               "<fanart>%s</fanart>" \
               "</item>" % (remove_non_ascii(group), xml_url, pic, addon_fanart)
    return xml


def wackenvod():
    name = "Wacken Youtube"
    url = "plugin://plugin.video.youtube/channel/UCvQT6N9nu2BJ-lJuMg1jEZQ/"
    icon = "http://static.wacken.com/images/woa2017/top-headerlogo-livestream-2017.png"
    fanart = "http://static.wacken.com/images/woa2017/bg-body.jpg"
    xml = "<plugin>" \
          "<title>%s</title>" \
          "<link>%s</link>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "</plugin>" % (name, url, icon, fanart)
    return xml


def graspopvod(url="http://vod.graspop.be"):
    html = BS(koding.Open_URL(url + "/?language=en"))
    stream_lis = html.findAll("li")
    xml = ""
    for stream_li in stream_lis:
        stream_channel_link = stream_li.find("a")
        try:
            group = stream_li.find("strong").text
            vodtype_type = stream_li.find("small").text
            group = group.replace(vodtype_type, "") +\
                " (%s)" % vodtype_type
            pic = stream_li.find("img")["src"]
        except:
            continue
        href = stream_channel_link["href"]
        xml_url = "play_channel({})".format("http://vod.graspop.be" + href)
        fanart = "https://www.graspop.be/assets/default/images/src/vod_background.jpg"
        xml += "<item>" \
               "<title>%s</title>" \
               "<midstock>%s</midstock>"\
               "<thumbnail>%s</thumbnail>" \
               "<fanart>%s</fanart>" \
               "</item>" % (remove_non_ascii(group), xml_url, pic, fanart)
    return xml


def werchtervod(url="http://vod.rockwerchter.be"):
    xml = ""
    html = BS(koding.Open_URL(url + "/?language=en"))
    stream_lis = html.findAll(
        "div", attrs={"class": re.compile(".*vod-list__item.*")})
    for stream_li in stream_lis:
        stream_channel_link = stream_li.find("a")
        group = stream_li["data-name"]
        vodtype_type = stream_li.find(
            "p", attrs={"class": re.compile(".*c-card__time.*")}).text
        label = group + " (%s)" % vodtype_type.strip()
        style = stream_li.find(
            "div", attrs={"class": re.compile(".*c-card__img.*")})["style"]
        pic = style.replace('background-image: url("', "").replace('");', "")
        href = stream_channel_link["href"]
        xml_url = "play_channel({})".format("http://vod.rockwerchter.be" +
                                            href)
        xml += "<item>" \
               "<title>%s</title>" \
               "<midstock>%s</midstock>"\
               "<thumbnail>%s</thumbnail>" \
               "<fanart>%s</fanart>" \
               "</item>" % (remove_non_ascii(label), xml_url, pic, addon_fanart)
    return xml


def remove_non_ascii(text):
    return unidecode(text)


def play_channel(url):
    html = koding.Open_URL(url + "&language=en")
    match = re.findall("hls:.*?'(.*?)'", html)
    for stream in match:
        if "bumper" in stream:
            continue
        koding.Play_Video(stream.replace("index-ios", "5"))
