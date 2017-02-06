from maya import OpenMaya, OpenMayaUI, OpenMayaAnim, cmds, mel


try:
    from PySide import QtCore
    from PySide import QtGui as gui
    import sys, os
    import shiboken

except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets as gui
    import shiboken2 as shiboken
    import sys, os

    
import platform
import subprocess
import urllib2
import zipfile
import shutil     
   

pointer = long(OpenMayaUI.MQtUtil.mainWindow())
maya_window = shiboken.wrapInstance(pointer, gui.QMainWindow) 

class BasicDialog (gui.QDialog):
    
    def __init__ (self, parent = maya_window): 
        super(BasicDialog, self).__init__(parent) 
        object_name = "LWS Character Manager" 

        exist = parent.findChild(gui.QDialog, object_name) 
        
        if exist:
            shiboken.delete (exist) 
            
        self.dir = cmds.internalVar(uwd = True)

        self.setWindowTitle( "LWS Character Manager" ) 
        self.setObjectName( object_name ) 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Tool)
   
        main_layout = gui.QVBoxLayout(self) 
        layout_labels = gui.QHBoxLayout(self)
        layout_button = gui.QVBoxLayout(self)
        layout_button2 = gui.QHBoxLayout(self)
        layout_button3 = gui.QHBoxLayout(self)
        layout_check = gui.QHBoxLayout(self)
        layout_dir = gui.QVBoxLayout(self)
        
        self.drop_file = gui.QComboBox()
        self.button_build = gui.QPushButton("Open File")
        self.button_refrence = gui.QPushButton("Refrence File")
        self.button_reloadRef = gui.QPushButton("Reload Char")
        self.button_save = gui.QPushButton("Set Project")
        self.button_openDir = gui.QPushButton("Open Directory")


        self.button_DownloadAll = gui.QPushButton("Install Characters")

        if os.path.exists(self.dir + 'LWS_Characters'): 
            self.button_DownloadAll.setText('Refresh Characters')
            self.button_refrence.setStyleSheet("background-color: grey")

        else:
            self.button_DownloadAll.setStyleSheet(("background-color:#639833;\
            border: 5px solid #639833")) 

        layout_button.addWidget(self.drop_file)
        map(layout_button2.addWidget, (self.button_refrence,self.button_save))
        map(layout_button3.addWidget, (self.button_build, self.button_reloadRef))
        map(layout_dir.addWidget,(self.button_openDir,self.button_DownloadAll))
        map(main_layout.addLayout, [layout_check, layout_button,layout_button2, layout_button3, layout_dir])
        
        #####################################################
        self.button_build.clicked.connect(self.build)
        self.button_save.clicked.connect(self.setProj)
        self.button_refrence.clicked.connect(self.refrenceFile)
        self.button_reloadRef.clicked.connect(self.reloadRef)
        self.button_openDir.clicked.connect(self.openDir)
        self.button_DownloadAll.clicked.connect(self.downloadCharacters);
        self.button_DownloadAll.clicked.connect(self.refreshUI)
        
        self.populateProjects()
        
    def refreshUI(self):
        import LWS_CharacterManager
        LWS_CharacterManager.UI()
    def populateProjects(self) :
               
        self.drop_file.clear()
        projects = []
        try:
            for fname in os.listdir(self.dir + 'LWS_Characters'):
                fpath = os.path.join(self.dir + 'LWS_Characters', fname)
                if os.path.isdir(fpath):
                   projects.append(fname)
            self.drop_file.addItems(projects)
        except:
            pass
        
    def setProj(self):
        selectedProject = str(self.drop_file.currentText())
        proj = self.dir + 'LWS_Characters/' + selectedProject
        cmds.workspace(dir = proj )
        cmds.workspace(proj, newWorkspace = True )
        cmds.workspace(proj, openWorkspace = True )
        cmds.workspace(proj, saveWorkspace = True )        
        
        
    def build(self):
        selectedProject = str(self.drop_file.currentText())
        for file in os.listdir(self.dir + 'LWS_Characters/' + selectedProject):
            if file.endswith(".ma"):
                mayaFile = file
        fileAll = self.dir + 'LWS_Characters/' + selectedProject + "/"  
        fileName = fileAll + mayaFile
        cmds.file(fileName, open = True, force = True, prompt = True)
        
    def refrenceFile(self):          
        selectedProject = str(self.drop_file.currentText())
        for file in os.listdir(self.dir + 'LWS_Characters/' + selectedProject):
            if file.endswith(".ma"):
                mayaFile = file
        fileAll = self.dir + 'LWS_Characters/' + selectedProject + "/"  
        fileName = fileAll + mayaFile
        cmds.file(fileName, ns = selectedProject, r = True, force = True, prompt = True)

    def reloadRef(self):
        selectedProject = str(self.drop_file.currentText())
        for file in os.listdir(self.dir + 'LWS_Characters/' + selectedProject):
            if file.endswith(".ma"):
                mayaFile = file
        fileAll = self.dir + 'LWS_Characters/' + selectedProject + "/"  
        sourceFile = fileAll + mayaFile
        scene = cmds.ls(references = True)
        print scene
        for refNode in scene:
            print refNode
            print sourceFile

            if selectedProject in refNode :
                cmds.file(sourceFile,loadReference = refNode , type = "mayaAscii",options = "v=0")

    def openDir(self):
        path = self.dir
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def downloadCharacters(self):
        try:
            url = 'https://www.dropbox.com/s/0ri5enj90ce7big/LWS_Characters.zip?dl=1'
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
            
            req = urllib2.Request(url, headers=hdr) 
                       
            folder = "LWS_Characters.zip"
            temp = cmds.internalVar(utd = True)
            fileName = temp + folder
            
            chunk_size=5000000
            gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
            cmds.progressBar( gMainProgressBar,
                            edit=True,
                            beginProgress=True,
                            isInterruptable=True,
                            status='Downloading Characters ...',
                            maxValue=100 )
            
            fileWrite = open(fileName, 'wb')
            response = urllib2.urlopen(req);
            self.total_size = response.info().getheader('Content-Length').strip()
            self.total_size = int(self.total_size)
            self.bytes_so_far = 0
            while 1:
                chunk = response.read(chunk_size)
                fileWrite.write(chunk)
                self.bytes_so_far += len(chunk)
                if not chunk:
                 break
                self.chunk_report()  
            cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
            fileWrite.close()
            sys.stdout.write('Unzipping file....');
            try:
                zip = zipfile.ZipFile(temp + 'LWS_Characters.zip')
                zip.extractall(self.dir)
            except:
                sys.stdout.write('could not unzip file....');
            sys.stdout.write('Files Installed!')
            self.populateProjects()

        except:
            confirm = cmds.confirmDialog( title='Install Failed', message='Would you like to view the HELP Doc for further instructions?', button=['OK'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if confirm == 'OK':
                cmds.launch(web="https://longwintermembers.com/help")

        
    def chunk_report(self):
        percent = float(self.bytes_so_far) / self.total_size
        percent = round(percent*100, 2)
        gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
        cmds.progressBar(gMainProgressBar, edit=True, progress=percent)
          
    
                            
def UI ():
    w=BasicDialog()
    w.show()
    
if __name__ == "__main__":
    UI()
    
