import urllib2
import maya.cmds as cmds
import maya.mel as mel
from os import listdir
from os.path import isfile, join
import zipfile
import shutil

def installScripts():
    scripts = cmds.internalVar(usd = True)
    temp = cmds.internalVar(utd = True)
    icons = cmds.internalVar(upd = True) + 'icons'
    shelves = cmds.internalVar(upd = True) + 'shelves'
    print shelves


    versionUrl = 'https://raw.githubusercontent.com/AndrewtConroy/characterTools/master/LWS_ToolsVersion.md'
    readVersion = urllib2.urlopen(versionUrl).read()
    readVersion = int(readVersion[-3:])

    versionFile = scripts + 'LWS_ToolsVersion.md'
    versionCheck = os.path.isfile(versionFile)
    updateVersion = False
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
        shelfFiles = os.listdir(scripts + 'characterTools-master/shelves/')
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
        
        #install shelves
        print shelfFiles
        for file in shelfFiles:
            shutil.copy(scripts + 'characterTools-master/shelves/' + file, shelves) 
         

        #rebuild and save shelf
        mel.eval('rehash;')
        try:
            mel.eval('loadNewShelf "shelf_LongWinter.mel";')
        except:
            mel.eval('loadNewShelf "shelf_LongWinter.mel";')

        mel.eval('saveAllShelves $gShelfTopLevel;')
        
installScripts()
import LWS_LicenseUI
reload(LWS_LicenseUI)
LWS_LicenseUI.UI()