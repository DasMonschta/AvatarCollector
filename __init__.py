from ts3plugin import ts3plugin
import ts3defines, os.path, shutil
import ts3lib as ts3
from ts3lib import getPluginPath
from os import path
from PythonQt.QtCore import *
from PythonQt.QtGui import *
from pytsonui import *

            
class AvatarCollector(ts3plugin):
    # --------------------------------------------
    # Plugin info vars
    # --------------------------------------------

    name            = "Avatar Collector"
    requestAutoload = False
    version         = "1.0"
    apiVersion      = 21
    author          = "Luemmel"
    description     = "Shows a list off all clientavatars. Klick on it for easy saving!"
    offersConfigure = True
    commandKeyword  = ""
    infoTitle       = None
    hotkeys         = []
    menuItems       = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Avatar Collector", "")]
    ac              = None
    
    def __init__(self):          
        pass
    def stop(self):
        pass     
        
    def configure(self, qParentWidget):
        self.ac = AvatarGallery(self)
        self.loadAvatars()
        self.ac.show()
        
    def onMenuItemEvent(self, sch_id, a_type, menu_item_id, selected_item_id):
        if a_type == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL:
            if menu_item_id == 0:               
                self.ac = AvatarGallery(self)
                self.loadAvatars()
                self.ac.show()
                
    def loadAvatars(self):
        pics = []
        schid = ts3.getCurrentServerConnectionHandlerID()
        err, clients = ts3.getClientList(schid)     
        
        for client in clients:
            err, avatar = ts3.getAvatar(schid, client, 256)
            if avatar != None:
                pics.append(avatar)   
        self.count = len(pics)
        self.ac.populate(pics)
        
class AvatarLabel(QLabel):    
    path = None
    destination = None
    
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)
        self.setMouseTracking(True)
        
    def mousePressEvent(self, event):      
        SaveFileDialog(self)
        if self.destination != "": 
            shutil.copy2(self.path, self.destination)

class SaveFileDialog(QFileDialog):
    def __init__(self, ac, parent=None):
        ac.destination = QFileDialog.getSaveFileName(self, 'Save avatar', os.path.expanduser("~")+"\\test.gif", "Images (*.png *.jpg *.gif);;All files (*.*)", Qt.WA_DeleteOnClose)

        
class AvatarGallery(QDialog):    
    def __init__(self, ac, parent=None):       
        
        self.ac = ac

        super(QDialog, self).__init__(parent)       
        self.setWindowIcon(QIcon(os.path.join(getPluginPath(), "pyTSon", "scripts", "avatarcollector", "icon.png")))
        setupUi(self, os.path.join(getPluginPath(), "pyTSon", "scripts", "avatarcollector", "main.ui"))
        self.setWindowTitle("Avatar Collector")
        
        # Load version from plguin vars
        self.ui_label_version.setText("v"+ac.version)
        
        # Delete QDialog on Close
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)        
     
        self.scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.ui_scroll_avatars.setWidget(self.scrollAreaWidgetContents)   
        
        # Reload Button connect
        self.ui_btn_reload.clicked.connect(ac.loadAvatars)
    
    def populate(self, pics, imagesPerRow=4, flags=Qt.KeepAspectRatioByExpanding):
        row = col = 0
        for pic in pics:
            label = AvatarLabel("")
            label.path = pic
            pixmap = QPixmap(pic)
            if self.ac.count == 1:          
                pixmap = pixmap.scaledToWidth(400, Qt.FastTransformation)
            else:
                pixmap = pixmap.scaledToWidth(100, Qt.FastTransformation)
            label.setPixmap(pixmap)
            self.gridLayout.addWidget(label, row, col)
            #self.layout().addWidget(label, row, col)
            col +=1
            if col % imagesPerRow == 0:
                row += 1
                col = 0
                
        self.ui_scroll_avatars.show()
        
        # Load results from plguin var
        self.ui_label_results.setText("Results: "+str(self.ac.count))

