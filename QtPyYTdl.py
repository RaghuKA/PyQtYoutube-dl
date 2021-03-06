from __future__ import unicode_literals
import os
import time
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
from PyQt5.QtCore import QObject, QProcess, QUrl, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QFileDialog, QAction, QPushButton, QVBoxLayout, QMessageBox, QToolTip
import functools 
import operator
from shutil import which
try:
    import youtube_dl
    is_youtubedl_installed = True
except ImportError as e:
    is_youtubedl_installed = False
import importlib.util
import time

glob_ui_file = "yTGui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(glob_ui_file)

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")
    
    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)
 
    def flush(self):
        pass  
                
class mywindow(QtWidgets.QMainWindow, Ui_MainWindow,Logger,QDialog):
    def __init__(self, dloadIpFile="", dloadDestDir=""):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setFixedSize(600, 400)
        
        self.setupUi(self)
                        
        self.dloadIpFile = dloadIpFile
        self.dloadDestDir = dloadDestDir
        
        self.FilePathField.setReadOnly(True)
        self.DloadDirPath.setReadOnly(True)
        self.Log.setReadOnly(True)
                              
        self.BrowseInputButton.clicked.connect(self.openFileNameDialog)
        self.BrowseDloaddirButton.clicked.connect(self.openFileNameDialog2)
        self.DloadVidsButton.clicked.connect(self.DownloadVideos)
        
        self.AboutButton.clicked.connect(self.openAction)

    def openAction(self):
        msg = "<br>Gui for youtube videos download"+"<br>'RaghuKA'"+"<br>'arkumar38@outlook.com'"+"<br> <a href='%s'>https://github.com/RaghuKA/PyQtYoutube-dl</a>" 
        QMessageBox.about(self, "About PyQtYouTube-dl", msg)
                         
    def openFileNameDialog(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Browse Input File", "", "Input Files (*.txt *.csv) ")
        self.FilePathField.setText (fileName)
        self.dloadIpFile = fileName
        self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> Input file specified as '+ self.dloadIpFile +'\n')
           
    def openFileNameDialog2(self):
        DloadDir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select directory')
        self.DloadDirPath.setText (DloadDir)
        self.dloadDestDir = DloadDir
        self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> Download destination directory chosen as '+ self.dloadDestDir +'\n')

    def DownloadVideos(self):
        if(is_youtubedl_installed == True):
            self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> youtube-dl is installed check complete\n')
            if os.path.exists(self.dloadDestDir):
                os.chdir(self.dloadDestDir)
                with open (self.dloadIpFile, 'r') as fh:     #Take test input file as 'videoslist.txt'
                    fh_list = fh.readlines ()
                    print(fh_list)
                    while ('\n' in fh_list):
                        fh_list.remove ('\n')
                    number_of_links = len(fh_list)
                    self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> Number of total download links is '+ str(number_of_links) + '\n')
                                                       
                for i in range (len (fh_list)):
                    video_link = fh_list[i].split (',') [0].strip()
                    custom_name = fh_list[i].split (',') [1].strip()
                    print(custom_name)
                    self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> Working on download link ' + str(i+1) +' of total '+ str(number_of_links) + '\n')
                    
                    if not custom_name:
                        ydl_opts = {
                            'outtmpl': '%(title)s.%(ext)s',
                            'writedescription': True,
                        }
                    else:
                        ydl_opts = {
                            'outtmpl': custom_name,
                            'writedescription': True,
                        }
                    sys.stdout = Logger()
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_link])
                    
                self.Log.insertPlainText('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> Download finished \n')
            else:
                print('The directory does not exist')
        else:
            self.Log.insertPlainText ('<'+time.strftime('%H:%M:%S%p %Z on %b %d, %Y')+'> The package youtube-dl is not installed. Install the package using pip install youtube_dl. Cannot download videos!')
        
if __name__ == "__main__":    
    app = QtWidgets.QApplication (sys.argv)
    window = mywindow ()
    window.show ()
    sys.exit (app.exec_())