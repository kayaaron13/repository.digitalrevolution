import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'Digital Revolution Wizard'
EXCLUDES       = [ADDON_ID, 'repository.digitalrevolution', 'plugin.program.digitalrevolutionwizard']
# Text File with build info in it.
BUILDFILE      = 'http://revolution-digital.net/wizard/txt/build.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 3
# Text File with apk info in it.
APKFILE        = 'http://revolution-digital.net/wizard/apks/'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = ''
YOUTUBEFILE    = 'http://'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://aftermathwizard.net/repo/wizard/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'http://revolution-digital.net/wizard/icons/kodibuilds.png'
ICONMAINT      = 'http://revolution-digital.net/wizard/icons/cleaning.png'
ICONAPK        = 'http://revolution-digital.net/wizard/icons/apk.png'
ICONADDONS     = 'http://revolution-digital.net/wizard/icons/installer.png'
ICONYOUTUBE    = 'http://revolution-digital.net/wizard/icons/youtube.png'
ICONSAVE       = 'http://revolution-digital.net/wizard/icons/save.png'
ICONTRAKT      = 'http://revolution-digital.net/wizard/icons/trakt.png'
ICONREAL       = 'http://revolution-digital.net/wizard/icons/realdebrid.png'
ICONLOGIN      = 'http://revolution-digital.net/wizard/icons/login.png'
ICONCONTACT    = 'http://revolution-digital.net/wizard/icons/contact.png'
ICONSETTINGS   = 'http://revolution-digital.net/wizard/icons/settings.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'Yes'
# Character used in seperator
SPACER         = '='

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'red'
COLOR2         = 'white'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']Digital Revolution[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Thank you for choosing Digital Revolution Wizard\r\nContact Me on twitter at @kayaaron13'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://'
CONTACTFANART  = 'http://'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = ''
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.digitalrevolution'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://revolution-digital.net/repository.digitalrevolution/zips/repository.digitalrevolution/addon.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://revolution-digital.net/repository.digitalrevolution/zips/repository.digitalrevolution/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'http://revolution-digital.net/wizard/txt/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = '[COLOR white]Digital Revolution Wizard[/COLOR]'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Background for Notification Window
BACKGROUND     = ''
#########################################################