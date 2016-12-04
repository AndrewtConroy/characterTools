import urllib2
import maya.cmds as cmds
import maya.mel as mel
import os
from os import listdir
from os.path import isfile, join
import zipfile
import shutil

def files():
    scripts = cmds.internalVar(usd = True)
    temp = cmds.internalVar(utd = True)
    icons = cmds.internalVar(upd = True) + 'icons'
    shelves = cmds.internalVar(upd = True) + 'shelves'
    versionUrl = 'https://raw.githubusercontent.com/AndrewtConroy/characterTools/master/LWS_ToolsVersion.md'
    readVersion = urllib2.urlopen(versionUrl).read()
    readVersion = int(readVersion[-3:])
    versionFile = scripts + 'LWS_ToolsVersion.md'
    versionCheck = os.path.isfile(versionFile)
    updateVersion = False
    scripts = cmds.internalVar(usd = True)
    scriptList = os.listdir(scripts)
    lwsScripts = ['LWS_SpeedPick.pyc','LWS_InstallScripts.py','LWS_LicenseUI.pyc','LWS_CharacterManager.pyc']
    for script in lwsScripts:
        if script not in scriptList :
            updateVersion = True

    if versionCheck == True:
        currentVersion = open(versionFile, 'r').read()
        currentVersion = int(currentVersion[-3:])
        
        if currentVersion < readVersion :
            updateVersion = True
        
    else: 
        updateVersion = True
        
    if updateVersion == True:
        print "copy all files"

        #download repo
        url = 'https://github.com/AndrewtConroy/characterTools/archive/master.zip'
        folder = "master.zip"
        fileName = temp + folder
        fileWrite = open(fileName, 'w')
        fileWrite.write(urllib2.urlopen(url).read())
        fileWrite.close()
        
        zip = zipfile.ZipFile(temp + 'master.zip')
        zip.extractall(scripts)
        
        scriptFiles = os.listdir(scripts + 'characterTools-master/scripts/')
        iconFiles = os.listdir(scripts + 'characterTools-master/icons/')
        shutil.copy(scripts + 'characterTools-master/' + 'LWS_ToolsVersion.md', scripts) 
        try:
            os.remove(scripts + '/characterTools-master')
        except:
            pass
        try:
            cmds.deleteUI('LongWinter', layout = True) 
            os.remove(shelves + '/shelf_LongWinter.mel')
            print shelves
        except:
            pass

        #install scripts
        print scriptFiles
        for file in scriptFiles:
            shutil.copy(scripts + 'characterTools-master/scripts/' + file, scripts) 
        #install icons
        print iconFiles
        for file in iconFiles:
            shutil.copy(scripts + 'characterTools-master/icons/' + file, icons) 
        
        mel.eval('rehash;')
        import LWS_LicenseUI 
        reload(LWS_LicenseUI) 
        LWS_LicenseUI.licenseNodes() 
        mel.eval('LWS_Menu;')

        
    
