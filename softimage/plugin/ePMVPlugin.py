
"""
    Copyright (C) <2010>  Autin L.
    
    This file ePMV_git/softimage/plugin/ePMVPlugin.py is part of ePMV.

    ePMV is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ePMV is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ePMV.  If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.
"""
# ePMVPlugin
# Initial code generated by Softimage SDK Wizard
# Executed Mon Sep 17 18:00:17 UTC+0200 2012 by jared.glass
# 
# Tip: To add a command to this plug-in, right-click in the 
# script editor and choose Tools > Add Command.
import win32com.client
from win32com.client import constants
#check path
import sys
#look for python
found = False
for p in sys.path:
	if p == "C:\Python26":
		found = True
try :
	import PyQt4
except :
	found = False
if not found :
	sys.path.insert(0,"C:\Python26")
	sys.path.insert(0,"C:\Python26\DLLs")
	sys.path.insert(0,"C:\Python26\libs")
	sys.path.insert(0,"C:\Python26\Lib")
	sys.path.insert(0,"C:\Python26\Lib\site-packages")
		
from PyQt4.QtGui import *

null = None
false = 0
true = 1
import siutils

import sys
found = True
try :
	import upy
except :
	found = False
if not found :
	#ys.path.append(__sipath__+'/MGLToolsPckgs/PIL')
	#sys.path.insert(0,__sipath__+'/MGLToolsPckgs/lib-tk')
	siutils.add_subfolder_to_syspath( __sipath__, '..\\MGLToolsPckgs' )
	siutils.add_subfolder_to_syspath( __sipath__, '..\\MGLToolsPckgs\\PIL' )
	siutils.add_subfolder_to_syspath( __sipath__, '..\\MGLToolsPckgs\\lib-tk' )
	sys.path.append(__sipath__+"\\..\\MGLToolsPckgs")
	MGL_ROOT=__sipath__+"\\..\\MGLToolsPckgs"
else :
	MGL_ROOT=upy.__path__[0]+"\\..\\"
import ePMV
import upy
upy.setUIClass('qt')
from ePMV import epmvGui

def XSILoadPlugin( in_reg ):
    in_reg.Author = "ludovic.autin"
    in_reg.Name = "ePMVPlugin"
    in_reg.Major = 1
    in_reg.Minor = 0

    in_reg.RegisterCommand("ePMV","ePMV")
    #RegistrationInsertionPoint - do not remove this line
    in_reg.RegisterMenu(constants.siMenuMainApplicationToolbarsID,"ePMV_Menu",false,false)
    return true

def XSIUnloadPlugin( in_reg ):
    strPluginName = in_reg.Name
    Application.LogMessage(str(strPluginName) + str(" has been unloaded."),constants.siVerbose)
    return true

def ePMV_Init( in_ctxt ):
    oCmd = in_ctxt.Source
    oCmd.Description = ""
    oCmd.ReturnValue = true

    return true

def ePMV_Execute(  ):

    Application.LogMessage("ePMV_Execute called",constants.siVerbose)
	
    import sip
    sianchor= Application.getQtSoftimageAnchor()
    sianchor= sip.wrapinstance( long(sianchor), QWidget )
    #dialog    = AnimationCopy_Dialog( sianchor )
    from upy.pythonUI import qtUI
    qtUI.mainRoot = sianchor    
    epmvui = epmvGui.epmvGui(parent=sianchor)
    epmvui.setup(rep="epmv",mglroot=MGL_ROOT,host='softimage')
    epmvui.epmv.Set(bicyl=True,use_progressBar = False,doLight = True,doCamera = True,
    useLog = False,doCloud=False,forceFetch=False)
    qtUI.mainRoot = epmvui
    epmvui.display()
    return true
	
def ePMV_Menu_Init( in_ctxt ):
	oMenu = in_ctxt.Source
	oMenu.AddCommandItem("ePMV","ePMV")
	return true	