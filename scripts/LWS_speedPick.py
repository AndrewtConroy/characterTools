###############################################################################
# Name: 
#   LWS_speedPick.py
#   LongWinterMembers.com 
#
###############################################################################

from maya import OpenMaya, OpenMayaUI, OpenMayaAnim, cmds, mel
from PySide import QtCore, QtGui
import shiboken, sys, os
import lws_rigUtils
reload(lws_rigUtils)

pointer = long(OpenMayaUI.MQtUtil.mainWindow())
maya_window = shiboken.wrapInstance(pointer, QtGui.QMainWindow)


class BasicDialog (QtGui.QDialog):
    def __init__ (self, parent=maya_window):
        super(BasicDialog, self).__init__(parent)
        object_name = "LWS_speedPick"

        exist = parent.findChild(QtGui.QDialog, object_name)
        
        if exist:
            shiboken.delete (exist)
            
        self.setWindowTitle( "LWS SpeedPick")
        self.setObjectName( object_name )
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Tool)

        imagePathBar = os.path.abspath(os.path.join (cmds.internalVar (upd=True) , "icons", "lws_SpeedPick-Bar.png")) 
        labelBar = QtGui.QLabel()
        imageBannerBar = QtGui.QPixmap(imagePathBar)
        labelBar.setPixmap(imageBannerBar)
        
        labelBar1 = QtGui.QLabel()
        imageBannerBar1 = QtGui.QPixmap(imagePathBar)
        labelBar1.setPixmap(imageBannerBar1)
        
        main_layout = QtGui.QVBoxLayout(self)
        layout_selection = QtGui.QHBoxLayout(self)
        layout_newSet = QtGui.QVBoxLayout(self)
        layout_addRemove = QtGui.QHBoxLayout(self)
        layout_addClear = QtGui.QHBoxLayout(self)
        layout_picker = QtGui.QHBoxLayout(self)
        layout_newName = QtGui.QHBoxLayout(self)

        self.name = QtGui.QLineEdit()
        self.name.setText('Enter NameSpace')
        self.name.textChanged.connect(self.reloadSets)
        
        self.diff_selection = QtGui.QComboBox()
        self.diff_selection.activated.connect(self.selectSet)
        selection_set_button = QtGui.QPushButton("Select Set")

        labelAdd = QtGui.QLabel(self)
        
        layout_utils1 = QtGui.QHBoxLayout(self)
        layout_utils2 = QtGui.QHBoxLayout(self)
        layout_utils3 = QtGui.QHBoxLayout(self)
        
        mirror_button = QtGui.QPushButton("Mirror")
        switch_button = QtGui.QPushButton("Switch")
        mirror_button.setStyleSheet("background-color: grey")
        switch_button.setStyleSheet("background-color: grey")

        selectMir_button = QtGui.QPushButton("SelectMirror")
        resetSel_button = QtGui.QPushButton("ResetSelected")
        selectMir_button.setStyleSheet("background-color: grey")
        resetSel_button.setStyleSheet("background-color: grey")
        
        resetAll_button = QtGui.QPushButton("ResetAll")
        default_button = QtGui.QPushButton("Default")
        resetAll_button.setStyleSheet("background-color: grey")
        default_button.setStyleSheet("background-color: grey")
        
        map(layout_utils1.addWidget, ( mirror_button,switch_button))
        map(layout_utils2.addWidget, ( selectMir_button,resetSel_button))
        map(layout_utils3.addWidget, ( resetAll_button,default_button))

        
        add_set_button = QtGui.QPushButton("Add to Set")
        remove_button = QtGui.QPushButton("Remove Set")
        removeObj_button = QtGui.QPushButton("Remove Obj")
        clear_button = QtGui.QPushButton("Clear Sets")
        buildPicker_button = QtGui.QPushButton("Build Picker")
        buildPicker_button.setStyleSheet("background-color: grey")

        self.name_selection = QtGui.QLineEdit()
        set_button = QtGui.QPushButton("+")
        set_button.setMaximumSize(QtCore.QSize(20, 20))
        map(layout_selection.addWidget, ( self.name_selection,set_button))
        layout_newSet.addWidget ( self.diff_selection)
        layout_newName.addWidget( self.name)
        map(layout_addRemove.addWidget,(add_set_button, removeObj_button))
        map(layout_addClear.addWidget,( remove_button, clear_button))
        layout_picker.addWidget( buildPicker_button)
        map(main_layout.addLayout, [layout_picker,layout_newSet, layout_selection,layout_addRemove, layout_addClear])
        main_layout.addWidget(labelBar)
        map(main_layout.addLayout, [layout_utils1,layout_utils2,layout_utils3])


        layout_slider = QtGui.QHBoxLayout(self)
        layout_button = QtGui.QHBoxLayout(self)
        
        
        self.nb_slider = QtGui.QLineEdit()
        self.nb_slider.setText('0')
        self.nb_slider.setMaximumWidth(40)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        pstnSlider = self.slider.value()
        inteSlider = int(pstnSlider)
        uniSlider = unicode(inteSlider)
        self.nb_slider.setText(uniSlider)
        map(layout_slider.addWidget, (self.nb_slider, self.slider))
        
        block_button = QtGui.QPushButton("Stepped")
        spline_button = QtGui.QPushButton("Spline")
        map(layout_button.addWidget, (block_button,spline_button))


        main_layout.addWidget(labelBar1)
        map(main_layout.addLayout, [layout_slider,layout_button])
              
        layout_image = QtGui.QHBoxLayout(self)
        layout_buttons = QtGui.QHBoxLayout(self)

        self.numb = QtGui.QLineEdit()
        self.numb.setMaximumSize(QtCore.QSize(20, 40))

        self.numb.setText('1')
        
        snap_button = QtGui.QPushButton("Snap")  
        snap_button.setMinimumSize(QtCore.QSize(150, 40))
        snap_button.clicked.connect(self.parentCons)
        
        map(layout_buttons.addWidget,(snap_button,self.numb))
        map(main_layout.addLayout,(layout_image,layout_buttons))
                
        main_layout.addLayout(layout_newName)
   
        set_button.clicked.connect(self.createSet)
        set_button.clicked.connect(self.reloadSets)
        add_set_button.clicked.connect(self.addSets)
        clear_button.clicked.connect(self.clearSets)
        remove_button.clicked.connect(self.removeSet)
        buildPicker_button.clicked.connect(self.buildPicker)
        removeObj_button.clicked.connect(self.removeObj)
        self.name_selection.returnPressed.connect(set_button.click)
        
        mirror_button.clicked.connect(self.mirror)
        switch_button.clicked.connect(self.switch)
        selectMir_button.clicked.connect(self.selMir)
        resetSel_button.clicked.connect(self.resetSelected)
        resetAll_button.clicked.connect(self.reset)
        default_button.clicked.connect(self.default)

        spline_button.clicked.connect(self.spline)
        block_button.clicked.connect(self.block)
        self.slider.valueChanged.connect(self.changeText)
        self.slider.sliderReleased.connect(self.setKey)
        self.nb_slider.editingFinished.connect(self.changeSlider)

        userSets = []
        selected = cmds.ls(type = 'objectSet')
        for item in selected :
            if item[0:4] == "set_" :
                userSets.append(item)
        
        displaySets = []
        for item in userSets :
            item = item[4:]
            displaySets.append(item)
        self.diff_selection.addItems(displaySets)
        
    def reloadSets(self) :
        self.diff_selection.clear()
        userSets = []
        displaySets = []
        selected = cmds.ls(type = 'objectSet')
        nameSpace = self.name.text()
        
        for item in selected :
            if nameSpace == "Enter NameSpace" :
                if item[0:4] == "set_" :
                    userSets.append(item)
                    displaySets.append(item[4:])
                                       
            elif self.name == '' :
                if item[0:4] == "set_" :
                    userSets.append(item)
                    displaySets.append(item[4:])

            else :
                nameLen = len(nameSpace)
                end = nameLen + 4
                if item[0:end] == nameSpace + "set_" :
                    userSets.append(item)
                    displaySets.append(item[end:])

        self.diff_selection.addItems(displaySets)
                
    def removeSet(self) :
        selectedSet = self.diff_selection.currentText() 
        selectedIndex = self.diff_selection.findText(selectedSet)
        removeSet = self.diff_selection.removeItem(selectedIndex)
        
    def removeObj(self) :
        nameSpace = self.name.text()
        if nameSpace == "Enter NameSpace" :
            nameSpace = ''
        selectedSet = nameSpace + 'set_' + self.diff_selection.currentText()
        selectedControl = cmds.ls(sl=1)
        for item in selectedControl :
            cmds.sets(selectedControl, remove = nameSpace + selectedSet,)
        
    def addSets(self):
        nameSpace = self.name.text()
        if nameSpace == "Enter NameSpace" :
            nameSpace = ''
        cSelection = cmds.ls(sl=True)
        for set in cSelection:
            selectedSet = nameSpace + 'set_' + self.diff_selection.currentText() 
            cmds.sets(set, addElement = selectedSet)

            
    def createSet (self):
        nameSpace = self.name.text()
        if nameSpace == "Enter NameSpace" :
            nameSpace = ''
            
        name = nameSpace + "set_" + self.name_selection.text() 
        if name == "set_" :
            cmds.warning('Please name your set')
        else:
            name = cmds.sets(n=name)
            name_str = str(name)
            self.diff_selection.addItem(name)
            self.name_selection.clear()
        
    def clearSets(self) :
        self.diff_selection.clear()

    def selectSet (self):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            mod = True
        else :
            mod = False
        nameSpace = self.name.text()
        if nameSpace == "Enter NameSpace" :
            current_set = 'set_' + self.diff_selection.currentText()
            cmds.select( current_set, add = mod )
        elif self.name == '' :
            current_set = 'set_' + self.diff_selection.currentText()
            cmds.select( current_set )
        else :
            current_set = nameSpace + 'set_' + self.diff_selection.currentText()
            cmds.select( current_set )

            #utils buttons
    def switch(self) : 
        lws_rigUtils.switch(self) 
    def mirror(self) :
        lws_rigUtils.mirror(self) 
    def selMir(self) : 
        lws_rigUtils.selectMirror() 
    def resetSelected(self) : 
        lws_rigUtils.resetSelected() 
    def reset(self) : 
        lws_rigUtils.reset() 
    def default(self) : 
        lws_rigUtils.default()
        
        
    def buildPicker(self) :
                
        #Choose a text file
        projectPath = cmds.internalVar(usd = True)
        name = ''
        folderName = 'LWS_picker' + name + '.py'
        fileName = projectPath + folderName

        fileWrite = open(fileName, 'w')

        fileWrite.write('from maya import OpenMaya, OpenMayaUI, OpenMayaAnim, cmds \n')
        fileWrite.write('from PySide import QtCore, QtGui \n')
        fileWrite.write('import shiboken, sys, os \n')
        fileWrite.write('import lws_rigUtils \n')

        fileWrite.write('pointer = long(OpenMayaUI.MQtUtil.mainWindow())\n')
        fileWrite.write('maya_window = shiboken.wrapInstance(pointer, QtGui.QMainWindow) \n')

        fileWrite.write('class BasicDialog (QtGui.QDialog): \n')

        fileWrite.write('    def __init__ (self, parent=maya_window): \n')
        fileWrite.write('        super(BasicDialog, self).__init__(parent) \n')
        fileWrite.write('        object_name = "LWS_Picker" \n')

        fileWrite.write('        exist = parent.findChild(QtGui.QDialog, object_name) \n')
        fileWrite.write('        #deletes the window if it exists\n')
        fileWrite.write('        if exist:\n')
        fileWrite.write('            shiboken.delete (exist) \n')
                
        fileWrite.write('        #sets some basic window properties\n')
        fileWrite.write('        self.setWindowTitle( "LWS Picker" ) \n')
        fileWrite.write('        self.setObjectName( object_name ) \n')
        fileWrite.write('        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)\n')
        fileWrite.write('        self.setWindowFlags(QtCore.Qt.Tool)\n')
        
        fileWrite.write('        #sets up the banner - simular for all lws windows\n')
        fileWrite.write('        imagePath = os.path.abspath(os.path.join (cmds.internalVar (upd=True) , "icons", "lws_bannerSA.jpg")) \n')
        fileWrite.write('        label = QtGui.QLabel()\n')
        fileWrite.write('        imageBanner = QtGui.QPixmap(imagePath)\n')
        fileWrite.write('        label.setPixmap(imageBanner)\n')

        #base layouts
        fileWrite.write('        #main layout everything will be connected to\n')
        fileWrite.write('        self.main_layout = QtGui.QVBoxLayout(self) \n')


        
        userSets = []
        selected = cmds.ls(type = 'objectSet')
        nameSpace = self.name.text()
        
        controlList = [self.diff_selection.itemText(i) for i in range(self.diff_selection.count())]
        nameLen = len(nameSpace)
        end = 4

        for item in controlList :
            
            if nameSpace == "Enter NameSpace" :
                item ='' + item 
                userSets.append(item)
                    
            elif nameSpace == '' :
                item = '' + item
                userSets.append(item)
            else :
                end = nameLen + 4
                userSets.append(item)
        
        for item in userSets :
            fileWrite.write('        ' + item + '_button =  QtGui.QPushButton(\'' + item + '\') \n') 
            fileWrite.write('        ' + item + '_button.setMaximumSize(QtCore.QSize(100, 20)) \n') 
            fileWrite.write('        ' + item + '_button.clicked.connect(self.' + item + ')\n') 
            fileWrite.write('        self.main_layout.addWidget(' + item + '_button)\n') 
            
            checkEven = userSets.index(item) 
            if checkEven % 2 == 0  :
                fileWrite.write('        ' + item + '_button.setStyleSheet("background-color: grey") \n')
                
                

        for item in userSets:
            if nameSpace == 'Enter NameSpace' :
                
                fileWrite.write('    def ' +  item + '(self) : \n')
                fileWrite.write('        modifiers = QtGui.QApplication.keyboardModifiers()\n')
                fileWrite.write('        if modifiers == QtCore.Qt.ShiftModifier:\n')
                fileWrite.write('            mod = True\n')
                fileWrite.write('        else :\n')
                fileWrite.write('            mod = False\n')
                                
                fileWrite.write('        cmds.select(\'' + 'set_' + item + '\', add = mod ) \n')
            else :
                fileWrite.write('    def ' +  item + '(self) : \n')
                fileWrite.write('        cmds.select(\'' + nameSpace + 'set_' + item + '\') \n')
    

        
        #writes the closing bits for the UI
        fileWrite.write('def UI ():\n')
        fileWrite.write('    w=BasicDialog()\n')
        fileWrite.write('    w.show()\n')
            
        fileWrite.write('if __name__ == "__main__":\n')
        fileWrite.write('    UI()\n')
        

        fileWrite.close()
        
        import LWS_picker
        reload(LWS_picker)
        LWS_picker.UI()
        
    def spline (self):
        if self.linearCheck.isChecked()==True :
            cmds.keyTangent( g=True, itt='linear', ott='linear' )
            current_selection = cmds.ls(sl=True)
            for obj in current_selection:
                cmds.keyTangent(obj, itt="linear", ott="linear")               
        else :
            cmds.keyTangent( g=True, itt='auto', ott='auto' )
            current_selection = cmds.ls(sl=True)
            for obj in current_selection:
                cmds.keyTangent(obj, itt="auto", ott="auto")
    def block (self):
        cmds.keyTangent( g=True, itt='clamped', ott='step' )
        current_selection = cmds.ls(sl=True)
        for obj in current_selection:
            cmds.keyTangent(obj,ott="step")
            
    def setKey(self):
        listObj = cmds.ls(sl=True)

        for current_selection in listObj:
            pstnSlider = self.slider.value()
            fltSlider = float(pstnSlider)
            inteSlider = int (fltSlider)
            pstnFact = inteSlider + 100
            pstnFact = float(pstnFact)
            factorNext = pstnFact / 200
            current_time = OpenMayaAnim.MAnimControl().currentTime().value ()
            current_time = int(current_time)
            channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
            list_custom_attr = cmds.channelBox(channelBox, q=True, sma=True)
            
            if list_custom_attr is None :
                att_object = cmds.listAttr(current_selection, k=True, u=True)
                if att_object is not None:
                    for obj in att_object:
                        name_attr = (str(current_selection) + "." + str(obj))
                        time_previous_key = cmds.findKeyframe( current_selection, timeSlider=True, which="previous" )
                        time_next_key = cmds.findKeyframe( current_selection, timeSlider=True, which="next" )
                        value_previous_key = cmds.keyframe ( name_attr, time = (time_previous_key,time_previous_key) , eval =True, query =True)
                        value_next_key = cmds.keyframe ( name_attr, time = (time_next_key,time_next_key) , eval =True, query =True)
                        difference_key = value_next_key[0] - value_previous_key[0]
                        factor_next_key =  difference_key * factorNext
                        inbetween_key = value_previous_key[0] + factor_next_key
                        cmds.setAttr(name_attr, inbetween_key)
                cmds.setKeyframe( current_selection, time = current_time)
            else:
                for obj in list_custom_attr:
                    name_attr = (str(current_selection) + "." + str(obj))
                    time_previous_key = cmds.findKeyframe( current_selection, timeSlider=True, which="previous" )
                    time_next_key = cmds.findKeyframe( current_selection, timeSlider=True, which="next" )
                    value_previous_key = cmds.keyframe ( name_attr, time = (time_previous_key,time_previous_key) , eval =True, query =True)
                    value_next_key = cmds.keyframe ( name_attr, time = (time_next_key,time_next_key) , eval =True, query =True)
                    difference_key = value_next_key[0] - value_previous_key[0]
                    factor_next_key =  difference_key * factorNext
                    inbetween_key = value_previous_key[0] + factor_next_key
                    cmds.setAttr(name_attr, inbetween_key)
                cmds.setKeyframe( current_selection, time = current_time)

    def changeText(self):
        pstnSlider = self.slider.value()
        fltSlider = float(pstnSlider)
        inteSlider = int (fltSlider)
        uniSlider = unicode(inteSlider)
        self.nb_slider.setText(uniSlider)
        
    
    def changeSlider(self):
        textSlider = self.nb_slider.text()
        fltText = float(textSlider)
        intText = int(fltText)
        self.slider.setValue(intText)


    def parentCons (self, *args):
        controls = cmds.ls(sl=1)
        children = controls[:-1]
        parent = controls[-1]
        aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')   
        selectionRange = cmds.timeControl(aPlayBackSliderPython, query=True, rangeArray=True)
        fstFrame = selectionRange[0]
        endFrame = selectionRange[1]
        if endFrame == fstFrame + 1 :
            fstFrame = cmds.playbackOptions(query=True, min=True)
            endFrame = cmds.playbackOptions(query=True, max=True)
                
        for item in children :
            parentOfItem = cmds.listRelatives(item, parent = 1)
            loc = cmds.spaceLocator(n='quickSnap_Loc_' + item)
            loc = loc[0]
            cmds.setAttr(loc + '.v',0)

            parentConstLoc = cmds.parentConstraint(item, loc, n = 'quickSnap_LocCon')
            cmds.delete(parentConstLoc)

            
            utils.snapPivot(parentOfItem, loc)
            parentConst = cmds.parentConstraint(parent, loc, n = 'quickSnapCon' + loc, mo=1)
            parentConstItem = cmds.parentConstraint(loc, item, n = 'quickSnapCon' + item, mo=1)
            
          
            number = self.numb.text()
            if number == '' :
                number = 1
            intNumb = int(number)
            cmds.bakeResults(item, t=(fstFrame,endFrame), sb=intNumb, simulation=True )
            cmds.delete(parentConst)
            cmds.delete(parentConstItem)
            cmds.delete(loc)
                
        
def UI ():
    w=BasicDialog()
    w.show()

if __name__ == "__main__":
    UI()