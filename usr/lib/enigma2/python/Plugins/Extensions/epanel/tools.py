# by 2boom 4bob@ua.fm 2011-14
# swap on hdd idea bigroma
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigIP, ConfigDateTime, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Harddisk import harddiskmanager
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Input import Input
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Console import Console as iConsole
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from time import *
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import new
import _enigma
import time
from time import localtime, strftime
import datetime
from os import environ
import os
import gettext

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("epanel", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/epanel/locale/"))

def _(txt):
	t = gettext.dgettext("epanel", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def mountp():
	pathmp = []
	if fileExists("/proc/mounts"):
		for line in open("/proc/mounts"):
			if "/dev/sd" in line:
				pathmp.append(line.split()[1].replace('\\040', ' ') + "/")
	pathmp.append("/usr/share/enigma2/")
	return pathmp
	
def remove_line(filename, what):
	if fileExists(filename):
		file_read = open(filename).readlines()
		file_write = open(filename, 'w')
		for line in file_read:
			if what not in line:
				file_write.write(line)
		file_write.close()

def insert_line(filename, what, numberline):
    if fileExists(filename):
        count_line = 1
        file_in = open(filename).readlines()
        file_out = open(filename, 'w')
        for line in file_in:
            if count_line is numberline:
                file_out.write(what)
            file_out.write(line)
            count_line += 1
        file_out.close()

def add_line(filename, what):
	if os.path.isfile(filename):
		with open(filename, 'a') as file_out:
			file_out.write(what)
			file_out.close()

def cronpath():
	path = "/etc/cron/crontabs/root"
	if fileExists("/etc/cron/crontabs"):
		return "/etc/cron/crontabs/root"
	elif fileExists("/etc/bhcron"):
		return "/etc/bhcron/root"
	elif fileExists("/etc/crontabs"):
		return "/etc/crontabs/root"
	elif fileExists("/var/spool/cron/crontabs"):
		return "/var/spool/cron/crontabs/root"
	return path

######################################################################################
config.plugins.epanel = ConfigSubsection()
config.plugins.epanel.scriptpath = ConfigSelection(default = "/usr/script/", choices = [
		("/usr/script/", _("/usr/script/")),
		("/media/hdd/script/", _("/media/hdd/script/")),
		("/media/usb/script/", _("/media/usb/script/")),
])
config.plugins.epanel.direct_source = ConfigSelection(default = "0", choices = [
		("0", _("linux-sat.tv")),
		("1", _("piconload.ru")),
])
config.plugins.epanel.direct = ConfigSelection(default = "/media/hdd/", choices = [
		("/media/hdd/", _("/media/hdd/")),
		("/media/usb/", _("/media/usb/")),
		("/usr/share/enigma2/", _("/usr/share/enigma2/")),
		("/tmp/", _("/tmp/")),
])
config.plugins.epanel.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.epanel.lang = ConfigSelection(default = "ru", choices = [
		("ru", _("Russian")),
		("ua", _("Ukrainian")),
		])
config.plugins.epanel.timedwn = ConfigClock(default = ((16*60) + 15) * 60) # 18:15
config.plugins.epanel.weekday = ConfigSelection(default = "0", choices = [
		("0", _("Mo")),
		("1", _("Tu")),
		("2", _("We")),
		("3", _("Th")),
		("4", _("Fr")),
		("5", _("Sa")),
		("6", _("Su")),
		])
config.plugins.epanel.min = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("5", "5"),
		("10", "10"),
		("15", "15"),
		("20", "20"),
		("25", "25"),
		("30", "30"),
		("35", "35"),
		("40", "40"),
		("45", "45"),
		("50", "50"),
		("55", "55"),
		])
config.plugins.epanel.hour = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", "0"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		])
config.plugins.epanel.dayofmonth = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		("24", "24"),
		("25", "25"),
		("26", "26"),
		("27", "27"),
		("28", "28"),
		("29", "29"),
		("30", "30"),
		("31", "31"),
		])
config.plugins.epanel.month = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", _("Jan.")),
		("2", _("Feb.")),
		("3", _("Mar.")),
		("4", _("Apr.")),
		("5", _("May")),
		("6", _("Jun.")),
		("7", _("Jul")),
		("8", _("Aug.")),
		("9", _("Sep.")),
		("10", _("Oct.")),
		("11", _("Nov.")),
		("12", _("Dec.")),
		])
config.plugins.epanel.dayofweek = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", _("Su")),
		("1", _("Mo")),
		("2", _("Tu")),
		("3", _("We")),
		("4", _("Th")),
		("5", _("Fr")),
		("6", _("Sa")),
		])
config.plugins.epanel.command = ConfigText(default="/usr/bin/", visible_width = 70, fixed_size = False)
config.plugins.epanel.every = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Min")),
		("2", _("Hour")),
		("3", _("Day of month")),
		("4", _("Month")),
		("5", _("Day of week")),
		])
config.plugins.epanel.manual = ConfigSelection(default = '0', choices = [
		('0', _("Auto")),
		('1', _("Manual")),
		])
config.plugins.epanel.manualserver = ConfigText(default="ntp.ubuntu.com", visible_width = 70, fixed_size = False)
config.plugins.epanel.server = ConfigSelection(default = "ua.pool.ntp.org", choices = [
		("ao.pool.ntp.org",_("Angola")),
		("1.az.pool.ntp.org",_("Azerbaidjan")),
		("mg.pool.ntp.org",_("Madagascar")),
		("za.pool.ntp.org",_("South Africa")),
		("tz.pool.ntp.org",_("Tanzania")),
		("bd.pool.ntp.org",_("Bangladesh")),
		("cn.pool.ntp.org",_("China")),
		("hk.pool.ntp.org",_("Hong Kong")),
		("in.pool.ntp.org",_("India")),
		("id.pool.ntp.org",_("Indonesia")),
		("ir.pool.ntp.org",_("Iran")),
		("jp.pool.ntp.org",_("Japan")),
		("kz.pool.ntp.org",_("Kazakhstan")),
		("kr.pool.ntp.org",_("Korea")),
		("my.pool.ntp.org",_("Malaysia")),
		("pk.pool.ntp.org",_("Pakistan")),
		("ph.pool.ntp.org",_("Philippines")),
		("sg.pool.ntp.org",_("Singapore")),
		("tw.pool.ntp.org",_("Taiwan")),
		("th.pool.ntp.org",_("Thailand")),
		("tr.pool.ntp.org",_("Turkey")),
		("ae.pool.ntp.org",_("United Arab Emirates")),
		("uz.pool.ntp.org",_("Uzbekistan")),
		("vn.pool.ntp.org",_("Vietnam")),
		("at.pool.ntp.org",_("Austria")),
		("by.pool.ntp.org",_("Belarus")),
		("be.pool.ntp.org",_("Belgium")),
		("bg.pool.ntp.org",_("Bulgaria")),
		("cz.pool.ntp.org",_("Czech Republic")),
		("dk.pool.ntp.org",_("Denmark")),
		("ee.pool.ntp.org",_("Estonia")),
		("fi.pool.ntp.org",_("Finland")),
		("fr.pool.ntp.org",_("France")),
		("de.pool.ntp.org",_("Germany")),
		("gr.pool.ntp.org",_("Greece")),
		("hu.pool.ntp.org",_("Hungary")),
		("ie.pool.ntp.org",_("Ireland")),
		("it.pool.ntp.org",_("Italy")),
		("lv.pool.ntp.org",_("Latvia")),
		("lt.pool.ntp.org",_("Lithuania")),
		("lu.pool.ntp.org",_("Luxembourg")),
		("mk.pool.ntp.org",_("Macedonia")),
		("md.pool.ntp.org",_("Moldova")),
		("nl.pool.ntp.org",_("Netherlands")),
		("no.pool.ntp.org",_("Norway")),
		("pl.pool.ntp.org",_("Poland")),
		("pt.pool.ntp.org",_("Portugal")),
		("ro.pool.ntp.org",_("Romania")),
		("ru.pool.ntp.org",_("Russian Federation")),
		("sk.pool.ntp.org",_("Slovakia")),
		("si.pool.ntp.org",_("Slovenia")),
		("es.pool.ntp.org",_("Spain")),
		("se.pool.ntp.org",_("Sweden")),
		("ch.pool.ntp.org",_("Switzerland")),
		("ua.pool.ntp.org",_("Ukraine")),
		("uk.pool.ntp.org",_("United Kingdom")),
		("bs.pool.ntp.org",_("Bahamas")),
		("ca.pool.ntp.org",_("Canada")),
		("gt.pool.ntp.org",_("Guatemala")),
		("mx.pool.ntp.org",_("Mexico")),
		("pa.pool.ntp.org",_("Panama")),
		("us.pool.ntp.org",_("United States")),
		("au.pool.ntp.org",_("Australia")),
		("nz.pool.ntp.org",_("New Zealand")),
		("ar.pool.ntp.org",_("Argentina")),
		("br.pool.ntp.org",_("Brazil")),
		("cl.pool.ntp.org",_("Chile")),
		])
config.plugins.epanel.onoff = ConfigSelection(default = '0', choices = [
		('0', _("No")),
		('1', _("Plugin")),
		('2', _("Cron")),
		])
config.plugins.epanel.time = ConfigSelection(default = "30", choices = [
		("30", _("30 min")),
		("1", _("60 min")),
		("2", _("120 min")),
		("3", _("180 min")),
		("4", _("240 min")),
		])
config.plugins.epanel.TransponderTime = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('1', _("On")),
		])
config.plugins.epanel.cold = ConfigSelection(default = '0', choices = [
		('0', _("No")),
		('1', _("Yes")),
		])
config.plugins.epanel.autosave = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('29', _("30 min")),
		('59', _("60 min")),
		('119', _("120 min")),
		('179', _("240 min")),
		])
config.plugins.epanel.droptime = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('1', _("60 min")),
		('2', _("120 min")),
		('3', _("180 min")),
		])
config.plugins.epanel.dropmode = ConfigSelection(default = '1', choices = [
		('1', _("free pagecache")),
		('2', _("free dentries and inodes")),
		('3', _("free pagecache, dentries and inodes")),
		])
config.plugins.epanel.autobackup = ConfigYesNo(default = False)
config.plugins.epanel.checkepgfile = ConfigYesNo(default = False)
config.plugins.epanel.e2shpatch = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.epanel.ipadr = NoSave(ConfigIP(default = [0,0,0,0]))
config.plugins.epanel.hostname = NoSave(ConfigText(default='', visible_width = 150, fixed_size = False))
config.plugins.epanel.alias = NoSave(ConfigText(default='', visible_width = 150, fixed_size = False))
######################################################################################
class ToolsScreen2(Screen):
	skin = """
	<screen name="ToolsScreen2" position="center,160" size="750,370" title="Service Tools">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.setTitle(_("Service Tools"))
		self.indexpos = None
		self["shortcuts"] = NumberActionMap(["ShortcutActions", "WizardActions", "NumberActions"],
		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"1": self.go,
			"2": self.go,
			"3": self.go,
			"4": self.go,
			"5": self.go,
			"6": self.go,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/crash.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/info2.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/epg.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/vset.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/script.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/ntp.png"))
		self.list.append((_("Crashlog viewer"), 1, _("view & remove crashlog files"), onepng ))
		self.list.append((_("View settings"), 2, _("view system settings"), fourpng ))
		self.list.append((_("System info"), 3, _("system info (free, dh -f, hosts)"), twopng ))
		self.list.append((_("EPG Downloader"), 4, _("Download EPG from  linux-sat.tv (exUSSR)"), treepng ))
		self.list.append((_("Synchronization NTP"), 5, _("Synchronization ntp every 30 min,60 min,120 min, 240 min and Now"), sixpng ))
		self.list.append((_("User Scripts"), 6, _("Start scripts from /usr/script"), fivepng ))
		if self.indexpos != None:
			self["menu"].setIndex(self.indexpos)
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def go(self, num = None):
		if num is not None:
			num -= 1
			if not num < self["menu"].count():
				return
			self["menu"].setIndex(num)
		item = self["menu"].getCurrent()[1]
		self.select_item(item)

	def keyOK(self, item = None):
		self.indexpos = self["menu"].getIndex()
		if item == None:
			item = self["menu"].getCurrent()[1]
			self.select_item(item)

	def select_item(self, item):
		if item:
			if item is 1:
				self.session.open(CrashLogScreen)
			elif item is 2:
				self.session.open(ViewSet)
			elif item is 3:
				self.session.open(Info2Screen)
			elif item is 4:
				self.session.open(epgdn)
			elif item is 5:
				self.session.open(NTPScreen)
			elif item is 6:
				self.session.open(ScriptScreen2)
			else:
				self.close(None)
######################################################################################
class ServiceMan(Screen):
	skin = """
<screen name="ServiceMan" position="center,160" size="750,370" title="Service Manager">
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" itemHeight="25" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.setTitle(_("Service Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "DirectionActions"],

		{
			"cancel": self.cancel,
			"back": self.cancel,
			"red": self.stopservice,
			"green": self.startservice,
			"yellow": self.restartservice,
		})
		self["key_red"] = StaticText(_("Stop"))
		self["key_green"] = StaticText(_("Start"))
		self["key_yellow"] = StaticText(_("ReStart"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		self.list.append((_("Manage Networking service"), "networking"))
		self.list.append((_("Manage Internet superserver (inetd)"), "inetd.busybox"))
		self.list.append((_("Manage Syslog/klogd service"), "syslog.busybox"))
		self.list.append((_("Manage Dropbear SSH service"), "dropbear"))
		self.list.append((_("Manage BusyBox-Cron service"), "busybox-cron"))
		if fileExists('/etc/init.d/udpxy.sh') and fileExists('/usr/bin/udpxy'):
			self.list.append((_("Manage UdPrxy service"), "udpxy.sh"))
		if fileExists('/etc/init.d/livestreamersrv'):
			self.list.append((_("Manage Livestreamer service"), "livestreamersrv"))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"cancel": self.close}, -1)

	def restartservice(self):
		menu_item = self["menu"].getCurrent()[1]
		if menu_item is not None:
			self.iConsole.ePopen("/etc/init.d/%s restart" % menu_item, self.info_mess_1, menu_item)
			
	def info_mess_1(self, result, retval, extra_args):
		if retval is 0:
			self.session.open(MessageBox, _("Restarting %s service") % extra_args, type = MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.session.open(MessageBox, _("UnSuccessfull") , type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def startservice(self):
		menu_item = self["menu"].getCurrent()[1]
		if menu_item is not None:
			self.iConsole.ePopen("/etc/init.d/%s start" % menu_item, self.info_mess_2, menu_item)
			
	def info_mess_2(self, result, retval, extra_args):
		if retval is 0:
			self.session.open(MessageBox, _("Starting %s service") % extra_args, type = MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.session.open(MessageBox, _("UnSuccessfull"), type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def stopservice(self):
		menu_item = self["menu"].getCurrent()[1]
		if menu_item is not None:
			self.iConsole.ePopen("/etc/init.d/%s stop" % menu_item, self.info_mess_3, menu_item)
			
	def info_mess_3(self, result, retval, extra_args):
		if retval is 0:
			self.session.open(MessageBox, _("Stoping %s service") % extra_args, type = MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.session.open(MessageBox, _("UnSuccessfull"), type = MessageBox.TYPE_INFO, timeout = 4 )
			
	def cancel(self):
		self.close()
######################################################################################
class SwapScreen2(Screen):
	skin = """
		<screen name="SwapScreen2" position="center,160" size="750,370" title="Swap on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Swap on USB/HDD"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Menu,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.Menu()
		
	def del_fstab_swap(self, result, retval, extra_args):
		if retval is 0:
			remove_line('/etc/fstab', 'swap')
		
	def Menu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/swapminion.png"))
		if self.is_zram():
			if fileExists("/proc/swaps"):
				for line in open("/proc/swaps"):
					if "media" in line:
						self.iConsole.ePopen("swapoff %s" % (line.split()[0]), self.del_fstab_swap)
			self.list.append((_("Zram swap is on"), _("press Close for Exit"), minispng, 'zram'))
		else:
			for line in mountp():
				if line not in "/usr/share/enigma2/":
					try:
						if self.swapiswork() in line:
							self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minisonpng, line))
						else:
							self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
					except:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.MenuDo, "cancel": self.close}, -1)
	
	def is_zram(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if "zram0" in line:
					return True
		return False
		
	def swapiswork(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if "media" in line:
					return line.split()[0][:-9]
		else:
			return " "
		
	def MenuDo(self):
		if "zram" in self["menu"].getCurrent()[3]:
			return
		swppath = self["menu"].getCurrent()[3] + "swapfile"
		self.session.openWithCallback(self.Menu,SwapScreen, swppath)
	
	def exit(self):
		self.close()
######################################################################################
class SwapScreen(Screen):
	skin = """
	<screen name="SwapScreen" position="center,160" size="750,370" title="Swap on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Swap on USB/HDD"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()


	def isSwapPossible(self):
		for line in open("/proc/mounts"):
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:-9]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return True
				else:
					return False
		return False
		
	def isSwapRun(self):
		if fileExists('/proc/swaps'):
			for line in open('/proc/swaps'):
				if self.swapfile in line:
					return True
			return False
		else:
			return False
			
	def isSwapSize(self):
		if fileExists(self.swapfile):
			swapsize = os.path.getsize(self.swapfile) / 1048576
			return ("%sMb" % swapsize)
		else:
			return ("N/A Mb")

	def createSwapFile(self, size):
		self.session.openWithCallback(self.CfgMenu, create_swap, self.swapfile, size)

	def removeSwapFle(self):
		self.iConsole.ePopen("rm -f %s" % self.swapfile, self.info_mess, _("Swap file removed"))

	def info_mess(self, result, retval, extra_args):
		self.setTitle(_("Swap on USB/HDD"))
		if retval is 0:
			self.mbox = self.session.open(MessageBox,extra_args, MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,_("Failure..."), MessageBox.TYPE_INFO, timeout = 6)
		self.CfgMenu()

	def offSwapFile_step1(self):
		remove_line('/etc/fstab', 'swap')
		self.iConsole.ePopen("swapoff %s" % self.swapfile, self.info_mess, _("Swap file stoped"))

	def onSwapFile_step1(self):
		self.iConsole.ePopen("swapoff %s" % self.swapfile, self.onSwapFile_step2)
		
	def onSwapFile_step2(self, result, retval, extra_args):
		remove_line('/etc/fstab', 'swap')
		with open('/etc/fstab', 'a') as fsatb_file:
			fsatb_file.write('%s/swapfile swap swap defaults 0 0\n' % self.swapfile[:10])
			fsatb_file.close()
		self.iConsole.ePopen("swapon %s" % self.swapfile, self.info_mess,_("Swap file started"))

	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/swapminion.png"))
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun():
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		self.setTitle(_("Please wait"))
		if self.isSwapPossible() == 1:
			m_choice = self["menu"].getCurrent()[1]
			if m_choice is "4":
				self.onSwapFile_step1()
			elif m_choice is "5":
				self.offSwapFile_step1()
			elif m_choice is "11":
				self.createSwapFile("131072")
			elif m_choice is "12":
				self.createSwapFile("262144")
			elif m_choice is "13":
				self.createSwapFile("524288")
			elif m_choice is "7":
				self.removeSwapFle()
		self.CfgMenu()
			
	def exit(self):
		self.close()
######################################################################################
SKIN_CSW = """
<screen name="create_swap" position="center,140" size="625,30" title="Please wait">
  <widget source="status" render="Label" position="10,5" size="605,22" zPosition="2" font="Regular; 20" halign="center" transparent="2" />
</screen>"""

class create_swap(Screen):
	def __init__(self, session, swapfile, size):
		Screen.__init__(self, session)
		self.session = session
		self.skin = SKIN_CSW
		self.swapfile = swapfile
		self.size = size
		self.setTitle(_("Please wait"))
		self["status"] = StaticText()
		self.iConsole = iConsole()
		self["status"].text = _("Creating...")
		self.iConsole.ePopen("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, self.size), self.makeSwapFile)
		
	def makeSwapFile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("mkswap %s" % self.swapfile, self.info_mess)
		else:
			self["status"].text = _("Failure...")
			self.iConsole.ePopen("sleep 4", self.end_func)
			
	def info_mess(self, result, retval, extra_args):
		if retval is 0:
			self["status"].text = _("Success...")
			self.iConsole.ePopen("sleep 4", self.end_func)
		else:
			self["status"].text = _("Failure...")
			self.iConsole.ePopen("sleep 4", self.end_func)

	def end_func(self, result, retval, extra_args):
		self.close()
######################################################################################
class UsbScreen(Screen):
	skin = """
<screen name="UsbScreen" position="center,160" size="750,370" title="Unmount manager">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Unmount manager"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.CfgMenu,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnMount"))
		self["key_yellow"] = StaticText(_("reFresh"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/usbico.png"))
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			try:
				for count in range(len(hddlist)):
					hdd = hddlist[count][1]
					devpnt = self.devpoint(hdd.mountDevice())
					if hdd.mountDevice() != '/media/hdd':
						if devpnt is not None:
							if int(hdd.free()) > 1024:
								self.list.append(("%s" % hdd.model(),"%s  %s  %s (%d.%03d GB free)" % (devpnt, self.filesystem(hdd.mountDevice()),hdd.capacity(), hdd.free()/1024 , hdd.free()%1024 ), minipng, devpnt))
							else:
								self.list.append(("%s" % hdd.model(),"%s  %s  %s (%03d MB free)" % (devpnt, self.filesystem(hdd.mountDevice()), hdd.capacity(),hdd.free()), minipng, devpnt))
			except:
				pass
		else:
			hddinfo = _("none")
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)

	def Ok(self):
		item = self["menu"].getCurrent()[-1]
		if item is not None:
			self.iConsole.ePopen("umount -f %s" % item, self.info_mess, item)

	def info_mess(self, result, retval, extra_args):
		if retval is 0:
			self.mbox = self.session.open(MessageBox,_("Unmounted %s" % extra_args), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def filesystem(self, mountpoint):
		if fileExists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if mountpoint in line:
					return "%s  %s" % (line.split()[2], line.split()[3].split(',')[0])
		return ''
			
	def devpoint(self, mountpoint):
		if fileExists("/proc/mounts"):
			for line in open("/proc/mounts"):
				if mountpoint in line:
					return line.split()[0]
		return ''
			
	def exit(self):
		self.close()
######################################################################################
class ScriptScreen2(Screen):
	skin = """
	<screen name="ScriptScreen2" position="center,160" size="750,370" title="Script Executer" >
		<widget name="list" position="20,10" size="710,305" scrollbarMode="showOnDemand" />
		<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.script, self.name = '', ''
		self.setTitle(_("Script Executer"))
		self.iConsole = iConsole()
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		if pathExists(config.plugins.epanel.scriptpath.value):
			list = os.listdir("%s" % config.plugins.epanel.scriptpath.value[:-1])
			list = [x[:-3] for x in list if x.endswith('.sh')]
		else:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		self.script = self["list"].getCurrent()
		if self.script is not None:
			self.name = "%s%s.sh" % (config.plugins.epanel.scriptpath.value, self.script)
			self.iConsole.ePopen("chmod 777 %s.sh" %  self.name, self.runScript)
			
	def runScript(self, result, retval, extra_args):
			self.session.open(Console, self.script.replace("_", " "), cmdlist=[self.name])

	def exit(self):
		self.close()
######################################################################################
class NTPScreen(ConfigListScreen, Screen):
	skin = """
<screen name="NTPScreen" position="center,160" size="750,370" title="NtpTime Updater">
		<widget position="15,10" size="720,200" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,358" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
		<widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="535,358" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" alphatest="blend" />
		<widget source="key_blue" render="Label" position="535,328" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.iConsole = iConsole()
		self.path = cronpath()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Update Now"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save_values,
			"yellow": self.UpdateNow,
			"blue": self.Manual,
			"ok": self.save_values
		}, -2)
		self.list.append(getConfigListEntry(_("NtpTime Updater"), config.plugins.epanel.onoff))
		self.list.append(getConfigListEntry(_("Set time to update"), config.plugins.epanel.time))
		self.list.append(getConfigListEntry(_("Set Transponder time update"), config.plugins.epanel.TransponderTime))
		self.list.append(getConfigListEntry(_("StartUp synchronization"), config.plugins.epanel.cold))
		self.list.append(getConfigListEntry(_("Set choice server mode"), config.plugins.epanel.manual))
		self.list.append(getConfigListEntry(_("Set your country"), config.plugins.epanel.server))
		self.list.append(getConfigListEntry(_("Set manual ntp server address"), config.plugins.epanel.manualserver))
		ConfigListScreen.__init__(self, self.list)
		self.onShow.append(self.Title)
		
	def Title(self):
		self.setTitle(_("NtpTime Updater"))

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()

	def Manual(self):
		self.session.open(ManualSetTime)

	def save_values(self):
		if not fileExists(self.path):
			open(self.path, 'a').close()
		if config.plugins.epanel.TransponderTime.value is '0': 
			config.misc.useTransponderTime.value = False
		else:
			config.misc.useTransponderTime.value = True
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		if fileExists('/etc/default/ntpdate'):
			file_read = open('/etc/default/ntpdate').readlines()
			file_write = open('/etc/default/ntpdate', 'w')
			for line in file_read:
				if 'NTPSERVERS="' in line:
					if config.plugins.epanel.manual.value is '0':
						file_write.write('NTPSERVERS="%s"\n' % config.plugins.epanel.server.value)
					else:
						file_write.write('NTPSERVERS="%s"\n' % config.plugins.epanel.manualserver.value)
				else:
					file_write.write(line)
			file_write.close() 
		if config.plugins.epanel.cold.value is not '0':
			if fileExists('/etc/rcS.d/S42ntpdate.sh'):
				os.remove('/etc/rcS.d/S42ntpdate.sh')
			if pathExists("/usr/bin/ntpdate-sync"):
				with open('/etc/rcS.d/S42ntpdate.sh', 'w') as start_script:
					start_script.write('#!/bin/sh\n\n[ -x /usr/bin/ntpdate-sync ] && /usr/bin/ntpdate-sync\n\nexit 0')
					start_script.close()
		if fileExists('/etc/rcS.d/S42ntpdate.sh'):
			os.chmod('/etc/rcS.d/S42ntpdate.sh', 0755)
		if config.plugins.epanel.onoff.value is '2':
			if fileExists(self.path):
				remove_line(self.path, 'ntpdate')
				self.cron_ntpsetup()
		else:
			if fileExists(self.path):
				remove_line(self.path, 'ntpdate')
			self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 6 )

	def cron_ntpsetup(self):
		with open(self.path, 'a') as cron_root:
			if config.plugins.epanel.time.value is "30":
				cron_root.write('*/30 * * * * /usr/bin/ntpdate-sync\n')
			else:
				cron_root.write('1 */%s * * * /usr/bin/ntpdate-sync\n' % config.plugins.epanel.time.value)
			cron_root.close()
		with open('%scron.update' % self.path[:-4], 'w') as cron_update:
			cron_update.write('root')
			cron_update.close()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 6 )

	def UpdateNow(self):
		self.session.open(update_current_time)

SKIN_UCT = """
<screen name="update_current_time" position="center,140" size="625,30" title="Please wait">
  <widget source="status" render="Label" position="10,5" size="605,22" zPosition="2" font="Regular; 20" halign="center" transparent="2" />
</screen>"""
class update_current_time(Screen):
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.skin = SKIN_UCT
		self.setTitle(_("Please wait"))
		self["status"] = StaticText()
		self.iConsole = iConsole()
		self["status"].text = _("synchronizing...")
		self.iConsole.ePopen("/usr/bin/ntpdate-sync", self.info_mess)

	def info_mess(self, result, retval, extra_args):
		if retval is 0:
			self["status"].text = _("Success...")
			self.iConsole.ePopen("sleep 4", self.end_func)
		else:
			self["status"].text = _("Failure...")
			self.iConsole.ePopen("sleep 4", self.end_func)

	def end_func(self, result, retval, extra_args):
		self.close()
#######################################################################################
class ManualSetTime(ConfigListScreen, Screen):
	skin = """
<screen name="ManualSetTime" position="center,160" size="750,370" title="NtpTime Updater">
	<widget position="15,10" size="720,200" name="config" />
	<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("NtpTime Updater"))
		self.timeinput_date = ConfigDateTime(default = time.time(), formatstring = _("%Y-%m-%d"), increment = 86400)
		self.timeinput_time = ConfigClock(default = time.time())
		self.newtime = self.getTimestamp(self.timeinput_date.value, self.timeinput_time.value)
		self.iConsole = iConsole()
		self.cfgMenu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save_timevalues,
			"ok": self.save_timevalues
		}, -2)
		
	def cfgMenu(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Set time"), self.timeinput_time))
		self.list.append(getConfigListEntry(_("Set date"), self.timeinput_date))
		ConfigListScreen.__init__(self, self.list)
		
	def getTimestamp(self, date, newtime):
		d = time.localtime(date)
		dt = datetime.datetime(d.tm_year, d.tm_mon, d.tm_mday, newtime[0], newtime[1])
		return int(time.mktime(dt.timetuple()))
		
	def save_timevalues(self):
		self.setTitle(_("Please wait"))
		self.newtime = self.getTimestamp(self.timeinput_date.value, self.timeinput_time.value)
		self.iConsole.ePopen("date -s %s" % time.strftime("%Y%m%d%H%M", time.localtime(self.newtime)), self.info_mess)
		
	def info_mess(self, result, retval, extra_args):
		if retval is 0:
			self.mbox = self.session.open(MessageBox,("%s" % time.strftime("%Y-%m-%d %H:%M", time.localtime(self.newtime))), MessageBox.TYPE_INFO, timeout = 6 )
		else:
			self.mbox = self.session.open(MessageBox,_("Failure..."), MessageBox.TYPE_INFO, timeout = 6)
		self.setTitle(_("NtpTime Updater"))
			
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
######################################################################################
class SystemScreen(Screen):
	skin = """
		<screen name="SystemScreen" position="center,160" size="750,370" title="System Tools">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.indexpos = None
		self.setTitle(_("System Tools"))
		self["shortcuts"] = NumberActionMap(["ShortcutActions", "WizardActions", "NumberActions"],
		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"1": self.go,
			"2": self.go,
			"3": self.go,
			"4": self.go,
			"5": self.go,
			"6": self.go,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/kernel.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/serviceman.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/unusb.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/swap.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/cron.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/hosts.png"))
		self.list.append((_("Kernel Modules Manager"), 1, _("load & unload kernel modules"), onepng))
		self.list.append((_("Service Manager"), 2, _("Start, Stop, Restart system services"), twopng))
		self.list.append((_("Cron Manager"), 3, _("Is a time-based job scheduler"), fivepng))
		self.list.append((_("Swap Manager"), 4, _("Start, Stop, Create, Remove Swap file"), fourpng ))
		self.list.append((_("UnMount USB"), 5, _("Unmount usb devices"), treepng ))
		self.list.append((_("Hosts editor"), 6, _("add/remove records in /etc/hosts"), sixpng ))
		if self.indexpos != None:
			self["menu"].setIndex(self.indexpos)
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def go(self, num = None):
		if num is not None:
			num -= 1
			if not num < self["menu"].count():
				return
			self["menu"].setIndex(num)
		item = self["menu"].getCurrent()[1]
		self.select_item(item)

	def keyOK(self, item = None):
		if item is None:
			item = self["menu"].getCurrent()[1]
			self.indexpos = self["menu"].getIndex()
			self.select_item(item)

	def select_item(self, item):
		if item:
			if item is 1:
				self.session.open(KernelScreen)
			elif item is 2:
				self.session.open(ServiceMan)
			elif item is 3:
				self.session.open(CrontabMan)
			elif item is 4:
				self.session.open(SwapScreen2)
			elif item is 5:
				self.session.open(UsbScreen)
			elif item is 6:
				self.session.open(HostsScreen)
			else:
				self.close(None)

######################################################################################
class KernelScreen(Screen):
	skin = """
<screen name="KernelScreen" position="center,100" size="750,570" title="Kernel Modules Manager">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="185,528" zPosition="2" size="210,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,558" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<ePixmap position="390,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="390,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="560,528" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="560,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.index = 0
		self.runmodule = ''
		self.module_list()
		self.setTitle(_("Kernel Modules Manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Load/UnLoad"))
		self["key_yellow"] = StaticText(_("LsMod"))
		self["key_blue"] = StaticText(_("Reboot"))
		self.list = []
		self["menu"] = List(self.list)
		
	def module_list(self):
		self.iConsole.ePopen('find /lib/modules/*/kernel/drivers/ | grep .ko', self.IsRunnigModDig)
		
	def BlueKey(self):
		self.session.open(TryQuitMainloop, 2)
		
	def YellowKey(self):
		self.session.open(lsmodScreen)
		
	def IsRunnigModDig(self, result, retval, extra_args):
		self.iConsole.ePopen('lsmod', self.run_modules_list, result)
		
	def run_modules_list(self, result, retval, extra_args):
		self.runmodule = ''
		if retval is 0:
			for line in result.splitlines():
				self.runmodule += line.split()[0].replace('-','_') + ' '
		self.CfgMenu(extra_args)
					
	def CfgMenu(self, result):
		self.list = []
		minipngmem = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/kernelminimem.png"))
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/kernelmini.png"))
		if result:
			for line in result.splitlines():
				if line.split('/')[-1][:-3].replace('-','_') in self.runmodule.replace('-','_'):
					self.list.append((line.split('/')[-1], line.split('kernel')[-1], minipngmem, line, True))
				else:
					self.list.append((line.split('/')[-1], line.split('kernel')[-1], minipng, line, False))
			self["menu"].setList(self.list)
			self["menu"].setIndex(self.index)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		module_name = ''
		module_name =  self["menu"].getCurrent()[-2].split('/')[-1][:-3]
		if not self["menu"].getCurrent()[-1]:
			self.load_module(module_name)
		else:
			self.unload_modele(module_name)
		self.index = self["menu"].getIndex()
		
	def unload_modele(self, module_name):
		self.iConsole.ePopen("modprobe -r %s" % module_name, self.rem_conf, module_name)
		
	def rem_conf(self, result, retval, extra_args):
		self.iConsole.ePopen('rm -f /etc/modules-load.d/%s.conf' % extra_args, self.info_mess, extra_args)
		
	def info_mess(self, result, retval, extra_args):
		self.mbox = self.session.open(MessageBox,_("UnLoaded %s.ko") % extra_args, MessageBox.TYPE_INFO, timeout = 4 )
		self.module_list()
		
	def load_module(self, module_name):
		self.iConsole.ePopen("modprobe %s" % module_name, self.write_conf, module_name)
		
	def write_conf(self, result, retval, extra_args):
		if retval is 0:
			with open('/etc/modules-load.d/%s.conf' % extra_args, 'w') as autoload_file:
				autoload_file.write('%s' % extra_args)
				autoload_file.close()
			self.mbox = self.session.open(MessageBox,_("Loaded %s.ko") % extra_args, MessageBox.TYPE_INFO, timeout = 4 )
			self.module_list()
		
	def exit(self):
		self.close()
######################################################################################
class lsmodScreen(Screen):
	skin = """
<screen name="lsmodScreen" position="center,100" size="750,570" title="Kernel Drivers in Memory">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.setTitle(_("Kernel Drivers in Memory"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()

	def CfgMenu(self):
		self.iConsole.ePopen('lsmod', self.run_modules_list)
		
	def run_modules_list(self, result, retval, extra_args):
		self.list = []
		aliasname = ''
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/kernelminimem.png"))
		if retval is 0:
			for line in result.splitlines():
				if len(line.split()) > 3:
					aliasname = line.split()[-1]
				else: 
					aliasname = ' '
				if 'Module' not in line:
					self.list.append((line.split()[0],( _("size: %s  %s") % (line.split()[1], aliasname)), minipng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)

	def exit(self):
		self.close()
######################################################################################
class CrashLogScreen(Screen):
	skin = """
<screen name="CrashLogScreen" position="center,160" size="750,370" title="View or Remove Crashlog files">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="530,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="530,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.path = config.plugins.epanel.crashpath.value
		self.setTitle(_("View or Remove Crashlog files"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("View"))
		self["key_yellow"] = StaticText(_("Remove"))
		self["key_blue"] = StaticText(_("Remove All"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/crashmini.png"))
		if pathExists(self.path):
			crashfiles = os.listdir(self.path)
			for line in crashfiles:
				if "enigma2_crash" in line:
					try:
						self.list.append((line,"%s" % time.ctime(os.path.getctime(self.path + line)), minipng))
					except:
						pass
		self.list.sort()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		if self["menu"].getCurrent()[0] is not None:
			item = self.path + self["menu"].getCurrent()[0]
			self.session.openWithCallback(self.CfgMenu,LogScreen, item)
	
	def YellowKey(self):
		if self["menu"].getCurrent()[0] is not None:
			item = self.path + self["menu"].getCurrent()[0]
			self.iConsole.ePopen("rm -f %s" % item, self.info_mess_1, item)
			
	def info_mess_1(self, result, retval, extra_args):
		if retval is 0:		
			self.mbox = self.session.open(MessageBox,(_("Removed %s") % extra_args), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def BlueKey(self):
		self.iConsole.ePopen("rm -f %senigma2_crash*.log" % self.path, self.info_mess_2)
			
	def info_mess_2(self, result, retval, extra_args):
		if retval is 0:	
			self.mbox = self.session.open(MessageBox,(_("Removed All Crashlog Files") ), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
######################################################################################
class LogScreen(Screen):
	skin = """
<screen name="LogScreen" position="center,80" size="1170,600" title="View Crashlog file">
	<ePixmap position="20,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,590" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="190,560" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="390,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="390,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="10,10" size="1150,542" font="Console;22" />
</screen>"""

	def __init__(self, session, what):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.crashfile = what
		self.setTitle(_("View Crashlog file"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self["key_yellow"] = StaticText(_("Save"))
		self["text"] = ScrollLabel("")
		self.listcrah()
		
	def exit(self):
		self.close()
	
	def GreenKey(self):
		self.session.open(TryQuitMainloop, 3)
		
	def YellowKey(self):
		self.iConsole.ePopen("gzip %s && mv %s.gz /tmp" % (self.crashfile, self.crashfile), self.info_create)
		
	def info_create(self, result, retval, extra_args):
		if retval is 0:
			self.mbox = self.session.open(MessageBox,_("%s.gz created in /tmp") % self.crashfile, MessageBox.TYPE_INFO, timeout = 4)
		else:
			self.mbox = self.session.open(MessageBox,_("Failure..."), MessageBox.TYPE_INFO, timeout = 4)
		
	def listcrah(self):
		list = ""
		with open(self.crashfile, "r") as files:
			for line in files:
				if "Traceback (most recent call last):" in line or "PC:" in line:
					for line in files:
						list += line
						if "]]>" in line:
							break
		self["text"].setText(list)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
SKIN_DWN = """
<screen name="get_epg_data" position="center,140" size="625,35" title="Please wait">
  <widget source="status" render="Label" position="10,5" size="605,22" zPosition="2" font="Regular; 20" halign="center" transparent="2" />
</screen>"""
class get_epg_data(Screen):
	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.skin = SKIN_DWN
		self.setTitle(_("Please wait"))
		self["status"] = StaticText()
		self.iConsole = iConsole()
		if config.plugins.epanel.direct_source.value is '0':
			source = 'linux-sat.tv'
		else:
			source = 'piconload.ru'
		self["status"].text = _("Donwloading epg.dat from %s" % source)
		self.download_epgfile()
		
	def download_epgfile(self):
		if config.plugins.epanel.direct_source.value is '0':
			self.iConsole.ePopen("wget -q 'http://linux-sat.tv/epg/epg_%s.dat.gz' -O %sepg.dat.gz" % (config.plugins.epanel.lang.value, config.plugins.epanel.direct.value), self.remove_epgfile)
		else:
			self.iConsole.ePopen("wget -q 'http://piconload.ru/upload/epg/epg_new.dat.gz' -O %sepg.dat.gz" % config.plugins.epanel.direct.value, self.remove_epgfile)
		
	def remove_epgfile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("mkdir -p %sepgtmp && rm -f %sepg.dat" % \
				(config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.copy_tmp)
		else:
			self.error_message()
		
	def copy_tmp(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.unpack_zip)
		else:
			self.error_message()
			
	def unpack_zip(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("gzip -df %sepg.dat.gz " % config.plugins.epanel.direct.value, self.attr_epgfile)
		else:
			self.error_message()
			
	def attr_epgfile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("chmod 644 %sepg.dat" % config.plugins.epanel.direct.value, self.loadepg)
		else:
			self.error_message()
			
	def loadepg(self, result, retval, extra_args):
		if retval is 0:
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
		else:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )
		self.close()
		
	def error_message(self):
		self["status"].text = _("error...")
		self.iConsole.ePopen("sleep 3", self.closeall)
	
	def closeall(self, result, retval, extra_args):
		self.close()
######################################################################################
class epgdn(ConfigListScreen, Screen):
	skin = """
<screen name="epgdn" position="center,160" size="750,370" title="EPG from linux-sat.tv (exUSSR)">
  <widget position="15,10" size="720,200" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,358" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,328" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG from linux-sat.tv/piconload.ru (exUSSR)"))
		self.iConsole = iConsole()
		self.list = []
		self.list.append(getConfigListEntry(_("Select source epg.dat"), config.plugins.epanel.direct_source))
		self.list.append(getConfigListEntry(_("Select path to save epg.dat"), config.plugins.epanel.direct))
		self.list.append(getConfigListEntry(_("Select EPG language"), config.plugins.epanel.lang))
		self.list.append(getConfigListEntry(_("Patch enigma2.sh (need restart enigma2)"), config.plugins.epanel.e2shpatch))
		self.list.append(getConfigListEntry(_("Restore EPG with enigma2 start"), config.plugins.epanel.coldstartepgrstore))
		self.list.append(getConfigListEntry(_("AutoDownload epg.dat"), config.plugins.epanel.auto))
		self.list.append(getConfigListEntry(_("AutoDownload time"), config.plugins.epanel.timedwn))
		self.list.append(getConfigListEntry(_("AutoDownload weekday"), config.plugins.epanel.weekday))
		self.list.append(getConfigListEntry(_("Automatic save/load EPG"), config.plugins.epanel.autosave))
		self.list.append(getConfigListEntry(_("Autobackup to ../epgtmp.gz"), config.plugins.epanel.autobackup))
		self.list.append(getConfigListEntry(_("Check if epg.dat exists"), config.plugins.epanel.checkepgfile))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Download EPG"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.download,
			"blue": self.manual,
			"ok": self.save
		}, -2)
		
	def download(self):
		self.session.open(get_epg_data)

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)

	def image_is_OA(self):
		if fileExists("/etc/issue"):
			for line in open("/etc/issue"):
				if 'openatv' in line or 'openhdf' in line or 'openvix' in line:
					return True
		return False

	def save(self):
		if self.image_is_OA():
			config.misc.epgcachefilename.value = "epg.dat"
			config.misc.epgcachepath.value = config.plugins.epanel.direct.value
			config.misc.epgcachepath.save()
			config.misc.epgcachefilename.save()
		
		config.misc.epgcache_filename.value = ("%sepg.dat" % config.plugins.epanel.direct.value)
		config.misc.epgcache_filename.save()

		for i in self["config"].list:
			i[1].save()
		configfile.save()
		if config.plugins.epanel.e2shpatch.value is "yes":
			ins_line = '[ -f %sepgtmp/epg.dat.gz ] && cp -f %sepgtmp/epg.dat.gz %s && gzip -df %sepg.dat.gz\n' %\
				(config.plugins.epanel.direct.value, config.plugins.epanel.direct.value, config.plugins.epanel.direct.value, config.plugins.epanel.direct.value)
			remove_line('/usr/bin/enigma2.sh', 'epg.dat')
			insert_line('/usr/bin/enigma2.sh', ins_line, 3)
		else:
			remove_line('/usr/bin/enigma2.sh', 'epg.dat')
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )

	def manual(self):
		self.session.open(epgdmanual)

	def restart(self):
		self.session.open(TryQuitMainloop, 3)
######################################################################################
class epgdmanual(Screen):
	skin = """
<screen name="epgdmanual" position="center,260" size="850,50" title="EPG from linux-sat.tv (exUSSR)">
  <ePixmap position="10,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="395,40" zPosition="1" size="220,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="395,10" zPosition="2" size="220,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="615,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="615,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
	def __init__(self, session):
		self.session = session
		self.iConsole = iConsole()
		Screen.__init__(self, session)
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save epg.dat"))
		self["key_yellow"] = StaticText(_("Restore epg.dat"))
		self["key_blue"] = StaticText(_("Reload epg.dat"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.savepg,
			"yellow": self.restepg,
			"blue": self.reload,
		}, -2)

	def reload(self):
		self.setTitle(_("Please wait"))
		if fileExists("%sepgtmp/epg.dat.gz" % config.plugins.epanel.direct.value):
			self.iConsole.ePopen("cp -f %sepgtmp/epg.dat.gz %s" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value), self.unpack_zip)
		
	def unpack_zip(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("gzip -df %sepg.dat.gz " % config.plugins.epanel.direct.value, self.attr_epgfile)
		else:
			self.error_message()
			
	def attr_epgfile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("chmod 644 %sepg.dat" % config.plugins.epanel.direct.value, self.reloadepg)
		else:
			self.error_message()
			
	def reloadepg(self, result, retval, extra_args):
		if retval is 0:
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("epg.dat reloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("reload epg.dat failed")), MessageBox.TYPE_INFO, timeout = 4 )
		self.setTitle(_("EPG from linux-sat.tv (exUSSR)"))

	def savepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		self.mbox = self.session.open(MessageBox,(_("epg.dat saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		self.mbox = self.session.open(MessageBox,(_("epg.dat restored")), MessageBox.TYPE_INFO, timeout = 4 )
	
	def error_message(self):
		self.mbox = self.session.open(MessageBox,(_("error...")), MessageBox.TYPE_INFO, timeout = 4 )
		self.cancel()
		
	def cancel(self):
		self.close(False)
######################################################################################
class CrontabMan(Screen):
	skin = """
<screen name="CrontabMan" position="center,160" size="750,370" title="CtronTab Manager - %s">
	<ePixmap position="20,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="195,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="195,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="370,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="370,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="15,15" size="720,288" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (700, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.path = cronpath()
		self.setTitle(_("CtronTab Manager - %s") % self.path)
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add tabs"))
		self["key_yellow"] = StaticText(_("Remove tabs"))
		self.list = []
		self["menu"] = List(self.list)
		self.cMenu()
		
	def cMenu(self):
		self.list = []
		if fileExists(self.path):
			for line in open(self.path):
				self.list.append((line, 0))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		self.close()
		
	def GreenKey(self):
		self.session.openWithCallback(self.cMenu,CrontabManAdd)
	
	def YellowKey(self):
		remove_line(self.path, self["menu"].getCurrent()[0])
		with open('%scron.update' % self.path[:-4], 'w') as cron_update:
			cron_update.write('root')
			cron_update.close()
		self.cMenu()
		
	def exit(self):
		self.close()
######################################################################################
class CrontabManAdd(ConfigListScreen, Screen):
	skin = """
<screen name="CrontabManAdd" position="center,160" size="750,370" title="add tabs - %s" >
	<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
	<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.path = cronpath()
		self.setTitle(_("add tabs - %s") % self.path)
		self.list = []
		self.list.append(getConfigListEntry(_("Min"), config.plugins.epanel.min))
		self.list.append(getConfigListEntry(_("Hour"), config.plugins.epanel.hour))
		self.list.append(getConfigListEntry(_("Day of month"), config.plugins.epanel.dayofmonth))
		self.list.append(getConfigListEntry(_("Month"), config.plugins.epanel.month))
		self.list.append(getConfigListEntry(_("Day of week"), config.plugins.epanel.dayofweek))
		self.list.append(getConfigListEntry(_("Command"), config.plugins.epanel.command))
		self.list.append(getConfigListEntry(_("Every"), config.plugins.epanel.every))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.ok,
			"ok": self.ok
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def ok(self):
		if not fileExists(self.path):
			open(self.path, 'a').close()
		everymin = everyhour = everydayofmonth = everymonth = everydayofweek = ""
		if config.plugins.epanel.min.value is not '*' and config.plugins.epanel.every.value is '1':
			everymin = '*/'
		elif config.plugins.epanel.hour.value is not '*' and config.plugins.epanel.every.value is '2':
			everyhour = '*/'
		elif config.plugins.epanel.dayofmonth.value is not '*' and config.plugins.epanel.every.value is '3':
			everydayofmonth = '*/'
		elif config.plugins.epanel.month.value is not '*' and config.plugins.epanel.every.value is '4':
			everymonth = '*/'
		elif config.plugins.epanel.dayofweek.value is not '*' and config.plugins.epanel.every.value is '5':
			everydayofweek = '*/'
		if config.plugins.epanel.min.value is '*' and config.plugins.epanel.hour.value is '*' and config.plugins.epanel.dayofmonth.value is '*' and config.plugins.epanel.month.value is '*' and  config.plugins.epanel.dayofweek.value is '*':
			print ("error")
		else:
			with open(self.path, 'a') as cron_root:
				cron_root.write('%s%s %s%s %s%s %s%s %s%s    %s' % (everymin, config.plugins.epanel.min.value, everyhour, config.plugins.epanel.hour.value,\
					everydayofmonth, config.plugins.epanel.dayofmonth.value, everymonth, config.plugins.epanel.month.value,\
					everydayofweek, config.plugins.epanel.dayofweek.value, config.plugins.epanel.command.value))
				cron_root.close()
			with open('%scron.update' % self.path[:-4], 'w') as cron_update:
				cron_update.write('root')
				cron_update.close()
		for i in self["config"].list:
			i[1].cancel()
		self.close()
######################################################################################
class Info2Screen(Screen):
	skin = """
<screen name="Info2Screen" position="center,100" size="890,560" title="System Info">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.setTitle(_("System Info"))
		self["text"] = ScrollLabel("")
		self["actions"] = ActionMap(["ShortcutActions", "WizardActions", "DirectionActions", "OkCancelActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"up": self["text"].pageUp,
			"left": self["text"].pageUp,
			"down": self["text"].pageDown,
			"right": self["text"].pageDown,
			})
		self["key_red"] = StaticText(_("Close"))
		self.infoall()
		
	def exit(self):
		self.close()
		
	def infoall(self):
		self.iConsole.ePopen("df -h", self.outinfo)
		
	def outinfo(self, result, retval, extra_args):
		list = ''
		int_Memtotal, int_Swaptotal = 0, 0
		if fileExists('/proc/meminfo'):
			for line in open('/proc/meminfo'):
				if 'MemTotal:' in line:
					list += 'MemTotal: %s Kb' % line.split()[-2]
					int_Memtotal = int(line.split()[-2])
				elif 'MemFree:' in line:
					list += '  MemFree: %s Kb  Used: %s Kb' % (line.split()[-2], int_Memtotal - int(line.split()[-2]))
				elif 'Buffers:' in line:
					list += '  Buffers: %s Kb\n' % line.split()[-2]
				elif 'SwapTotal:' in line:
					list += 'SwapTotal: %s Kb' % line.split()[-2]
					int_Swaptotal = int(line.split()[-2])
				elif 'SwapFree:' in line:
					list += '  SwapFree: %s Kb  Used: %s Kb\n\n' % (line.split()[-2], int_Swaptotal - int(line.split()[-2]))
		if retval is 0:
			for line in result.splitlines(True):
				list += line
		list += '\n'
		if fileExists('/etc/hosts'):
			for line in open('/etc/hosts'):
				if line.startswith('\n'):
					list += line.replace('\n', '')
				else:
					list += line
		self["text"].setText(list)

######################################################################################
class ViewSet(Screen):
	skin = """
<screen name="ViewSet" position="center,80" size="1170,600" title="View System Settings (/etc/enigma2/settings)">
	<ePixmap position="20,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="20,10" size="1130,542" font="Console;22" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("View System Settings (/etc/enigma2/settings)"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.viewsettings()
		
	def exit(self):
		self.close()
		
	def viewsettings(self):
		list = ''
		if fileExists("/etc/enigma2/settings"):
			for line in open("/etc/enigma2/settings"):
				list += line
		self["text"].setText(list)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"],
			{
			"cancel": self.close,
			"up": self["text"].pageUp,
			"left": self["text"].pageUp,
			"down": self["text"].pageDown,
			"right": self["text"].pageDown,
			},
			-1)
######################################################################################
class HostsScreen(Screen):
	skin = """
<screen name="HostsScreen" position="center,160" size="750,370" title="/etc/hosts editor">
	<ePixmap position="20,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="195,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="195,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="370,328" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="370,358" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="15,15" size="720,288" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (700, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.path = '/etc/hosts'
		self.setTitle(_("/etc/hosts editor"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
			{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
		},
		-1)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add record"))
		self["key_yellow"] = StaticText(_("Remove record"))
		self.list = []
		self["menu"] = List(self.list)
		self.cMenu()
		
	def cMenu(self):
		self.list = []
		if fileExists(self.path):
			for line in open(self.path):
				if not line.startswith('\n'):
					self.list.append((line, 0))
		self["menu"].setList(self.list)

	def Ok(self):
		self.close()
		
	def GreenKey(self):
		self.session.openWithCallback(self.cMenu,AddRecord)
		#self.close()
	
	def YellowKey(self):
		remove_line(self.path, self["menu"].getCurrent()[0])
		self.cMenu()
		
	def exit(self):
		self.close()

class AddRecord(ConfigListScreen, Screen):
	skin = """
<screen name="AddRecord" position="center,160" size="750,370" title="add record" >
	<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
	<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.path = cronpath()
		self.setTitle(_("add record"))
		self.list = []
		self.list.append(getConfigListEntry(_("ip address"), config.plugins.epanel.ipadr))
		self.list.append(getConfigListEntry(_("host name"), config.plugins.epanel.hostname))
		self.list.append(getConfigListEntry(_("alias"), config.plugins.epanel.alias))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.ok,
			"ok": self.ok
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def ok(self):
		ip_str = ''
		for digit in range(len(config.plugins.epanel.ipadr.value)):
			ip_str += '%s.' % config.plugins.epanel.ipadr.value[digit]
		ip_str = ip_str.rstrip('.')
		add_line('/etc/hosts', '%s\t%s\t\t%s\n' % (ip_str, config.plugins.epanel.hostname.value, config.plugins.epanel.alias.value))
		for i in self["config"].list:
			i[1].cancel()
		self.close()
######################################################################################
class System2Screen(Screen):
	skin = """
		<screen name="System2Screen" position="center,160" size="750,370" title="System Tools 2">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (120, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (130, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.indexpos = None
		self.setTitle(_("System Tools 2"))
		self["shortcuts"] = NumberActionMap(["ShortcutActions", "WizardActions", "NumberActions"],
		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"1": self.go,
			"2": self.go,
			"3": self.go,
			"4": self.go,
			"5": self.go,
			"6": self.go,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/epanel/images/drop.png"))
		self.list.append((_("Cache Flush"), 1, _("free pagecache, dentries and inodes"), onepng))
		if self.indexpos != None:
			self["menu"].setIndex(self.indexpos)
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def go(self, num = None):
		if num is not None:
			num -= 1
			if not num < self["menu"].count():
				return
			self["menu"].setIndex(num)
		item = self["menu"].getCurrent()[1]
		self.select_item(item)

	def keyOK(self, item = None):
		if item is None:
			item = self["menu"].getCurrent()[1]
			self.indexpos = self["menu"].getIndex()
			self.select_item(item)

	def select_item(self, item):
		if item:
			if item is 1:
				self.session.open(DropScreen)
			else:
				self.close(None)
######################################################################################
class DropScreen(ConfigListScreen, Screen):
	skin = """
<screen name="DropScreen" position="center,160" size="750,370" title="Cache Flush">
	<eLabel position="30,220" size="690,2" backgroundColor="#aaaaaa" />
	<widget position="15,10" size="720,200" name="config" scrollbarMode="showOnDemand" />
	<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="340,358" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/epanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="340,328" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="MemoryLabel" render="Label" position="55,235" size="150,22" font="Regular; 20" halign="right" foregroundColor="#aaaaaa" />
	<widget source="memTotal" render="Label" position="220,235" zPosition="2" size="450,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="bufCache" render="Label" position="220,260" zPosition="2" size="450,22" font="Regular;20" halign="left" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.list = []
		self.iConsole = iConsole()
		self.path = cronpath()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Flush Now"))
		self["memTotal"] = StaticText()
		self["bufCache"] = StaticText()
		self["MemoryLabel"] = StaticText(_("Memory:"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save_values,
			"yellow": self.ClearNow,
			"ok": self.save_values
		}, -2)
		self.list.append(getConfigListEntry(_("Autotime cache flush"), config.plugins.epanel.droptime))
		self.list.append(getConfigListEntry(_("Set cache flush mode"), config.plugins.epanel.dropmode))
		ConfigListScreen.__init__(self, self.list)
		self.onShow.append(self.Title)
		
	def Title(self):
		self.setTitle(_("Cache Flush"))
		self.infomem()

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def infomem(self):
		memtotal = memfree = buffers = cached = ''
		persent = 0
		if fileExists('/proc/meminfo'):
			for line in open('/proc/meminfo'):
				if 'MemTotal:' in line:
					memtotal = line.split()[1]
				elif 'MemFree:' in line:
					memfree = line.split()[1]
				elif 'Buffers:' in line:
					buffers = line.split()[1]
				elif 'Cached:' in line:
					cached = line.split()[1]
			if '' is not memtotal and '' is not memfree:
				persent = int(memfree) / (int(memtotal) / 100)
			self["memTotal"].text = _("Total: %s Kb  Free: %s Kb (%s %%)") % (memtotal, memfree, persent)
			self["bufCache"].text = _("Buffers: %s Kb  Cached: %s Kb") % (buffers, cached)

	def save_values(self):
		if not fileExists(self.path):
			open(self.path, 'a').close()
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		if fileExists(self.path):
			remove_line(self.path, 'drop_caches')
		if config.plugins.epanel.droptime.value is not '0':
			self.cron_setup()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )

	def cron_setup(self):
		if config.plugins.epanel.droptime.value is not '0':
			with open(self.path, 'a') as cron_root:
				cron_root.write('1 */%s * * * echo %s > /proc/sys/vm/drop_caches\n' % (config.plugins.epanel.droptime.value, config.plugins.epanel.dropmode.value))
				cron_root.close()
			with open('%scron.update' % self.path[:-4], 'w') as cron_update:
				cron_update.write('root')
				cron_update.close()

	def ClearNow(self):
		self.iConsole.ePopen("echo %s > /proc/sys/vm/drop_caches" % config.plugins.epanel.dropmode.value, self.Finish)
		
	def Finish(self, result, retval, extra_args):
		if retval is 0:
			self.mbox = self.session.open(MessageBox,(_("Cache flushed")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_("error...")), MessageBox.TYPE_INFO, timeout = 4 )
		self.infomem()
##################################################################################################