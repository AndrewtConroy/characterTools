import urllib2
import maya.cmds as cmds
import maya.mel as mel
import os
from os import listdir
from os.path import isfile, join
import zipfile
import shutil
import maya.OpenMaya as api

def userSetup():
    scripts = cmds.internalVar(usd = True)
    fileName = scripts + 'userSetup.py'
    if os.path.isfile(fileName) ==  True :
        fileText = open(fileName).read()
        if 'LWS_InstallScripts.installScripts' not in fileText :
            fileWrite = open(fileName, 'a')
            fileWrite.write('\n')
            fileWrite.write('import urllib2 \n')
            fileWrite.write('import maya.cmds as cmds \n')
            fileWrite.write('try: \n')
            fileWrite.write('   import LWS_InstallScripts \n')
            fileWrite.write('   reload(LWS_InstallScripts) \n')
            fileWrite.write('   LWS_InstallScripts.installScripts(run = True)\n')
            fileWrite.write('except: \n')
            fileWrite.write('   url = \'https://raw.githubusercontent.com/AndrewtConroy/characterTools/master/scripts/LWS_InstallScripts.py\' \n')
            fileWrite.write('   scripts = cmds.internalVar(usd = True) \n')
            fileWrite.write('   folder = "LWS_InstallScripts.py" \n')
            fileWrite.write('   fileName = scripts + folder \n')
            fileWrite.write('   fileWrite = open(fileName, \'w\') \n')
            fileWrite.write('   fileWrite.write(urllib2.urlopen(url).read()) \n')
            fileWrite.write('   fileWrite.close() \n')
            fileWrite.write('   import LWS_InstallScripts \n')
            fileWrite.write('   reload(LWS_InstallScripts) \n')
            fileWrite.write('   LWS_InstallScripts.installScripts(run = True)\n')
            fileWrite.close()
    else:
        fileWrite = open(fileName, 'w')
        fileWrite.write('\n')
        fileWrite.write('import urllib2 \n')
        fileWrite.write('import maya.cmds as cmds \n')
        fileWrite.write('try: \n')
        fileWrite.write('   import LWS_InstallScripts \n')
        fileWrite.write('   reload(LWS_InstallScripts) \n')
        fileWrite.write('   LWS_InstallScripts.installScripts(run = True)\n')
        fileWrite.write('except: \n')
        fileWrite.write('   url = \'https://raw.githubusercontent.com/AndrewtConroy/characterTools/master/scripts/LWS_InstallScripts.py\' \n')
        fileWrite.write('   scripts = cmds.internalVar(usd = True) \n')
        fileWrite.write('   folder = "LWS_InstallScripts.py" \n')
        fileWrite.write('   fileName = scripts + folder \n')
        fileWrite.write('   fileWrite = open(fileName, \'w\') \n')
        fileWrite.write('   fileWrite.write(urllib2.urlopen(url).read()) \n')
        fileWrite.write('   fileWrite.close() \n')
        fileWrite.write('   import LWS_InstallScripts \n')
        fileWrite.write('   reload(LWS_InstallScripts) \n')
        fileWrite.write('   LWS_InstallScripts.installScripts(run = True)\n')
        fileWrite.write('maya.mel.eval(\'LWS_Menu;\')\n')
        fileWrite.close()

def userSetupMel():
    scripts = cmds.internalVar(usd = True)
    fileName = scripts + 'userSetup.mel'
    if os.path.isfile(fileName) ==  True :
        fileText = open(fileName).read()
        if 'LWS_Menu;' not in fileText :
            fileWrite = open(fileName, 'a')
            fileWrite.write('LWS_Menu;')
            fileWrite.close()
    else:
        fileWrite = open(fileName, 'w')
        fileWrite.write('LWS_Menu;')
        fileWrite.close()
        
def installScripts(run = True):
    userSetup()
    userSetupMel()
    updateVersion = False
    scripts = cmds.internalVar(usd = True)
    temp = cmds.internalVar(utd = True)
    icons = cmds.internalVar(upd = True) + 'icons'
    shelves = cmds.internalVar(upd = True) + 'shelves'
    site = 'https://raw.githubusercontent.com/AndrewtConroy/characterTools/master/LWS_ToolsVersion.md'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    try:
        req = urllib2.Request(site, headers=hdr)
        page = urllib2.urlopen(req)
        version = page.read()
        page.close()
        print '::Long Winter Tools Version ' + version + '::'
        connected = True
    except urllib2.HTTPError, e:
        version = e.fp.read()        
        print version
        connected = False
            
    if connected == True:
        
        readVersion = int(version)
        versionFile = scripts + 'LWS_ToolsVersion.md'
        scripts = cmds.internalVar(usd = True)
        scriptList = os.listdir(scripts)
        lwsScripts = ['LWS_speedPick.pyc','LWS_InstallScripts.py','LWS_LicenseUI.pyc','LWS_Menu.mel','LWS_CharacterManager.py']
        for script in lwsScripts:
            if script not in scriptList :
                updateVersion = True
                
        if os.path.isfile(versionFile) == True:
            currentVersion = open(versionFile, 'r').read()
            currentVersion = int(currentVersion)
            if currentVersion < readVersion :
                updateVersion = True
        else: 
            updateVersion = True
        if updateVersion == True:
            print "::Updating Long Winter Tools::"
            try:
                shutil.rmtree(scripts + '\characterTools-master')
            except:
                print '::New Install::'
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

            for file in scriptFiles:
                shutil.copy(scripts + 'characterTools-master/scripts/' + file, scripts) 
            for file in iconFiles:
                shutil.copy(scripts + 'characterTools-master/icons/' + file, icons) 
        else:
            print "::Long Winter Tools are up to date::"
            
