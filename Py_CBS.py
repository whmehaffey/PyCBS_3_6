
import sys
from PyQt4.QtGui import QApplication,QDialog,QSizeGrip
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

##from PyRecordMenu import Ui_MainWindow
from AudioRecorderFunctions import *
import GlobalVars



def RescanInputsButtonPushed():
    
    import GlobalVars
    import pyaudio as pa
    
    inputdevices = 0
    
    pya = pa.PyAudio()
    info = pya.get_host_api_info_by_index(0)
    DeviceList = info.get('deviceCount')
    
    ui.InputSelectioncomboBox.clear();
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,DeviceList):
        #print(pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels'))
        if pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
             print(pya.get_device_info_by_host_api_device_index(0,i).get('name'))
            #if ((pya.get_device_info_by_host_api_device_index(0,i).get('name').find("Te"))!=-1):
             ui.InputSelectioncomboBox.insertItem(20,str(pya.get_device_info_by_host_api_device_index(0,i).get('name')))    
             inputdevices+=1
 

  
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0
    
    ui.StartPushButton.setEnabled(True)
    ui.RescanInputsPushButton.setEnabled(True)
    ui.ThresholdLineEdit.setEnabled(True)
    ui.BirdNameLineEdit.setEnabled(True)   
    ui.InputSelectioncomboBox.setEnabled(True)
    ui.WorkingDirpushButton.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)    
    ui.ListeningTextBox.setText('')
    ui.radioButton.setEnabled(True);
    
    if not GlobalVars.Stereo:
        GlobalVars.ThreshChan=1             # Set Mono, trigger on only channel
        ui.radioButton_2.setEnabled(False)
        ui.radioButton_3.setEnabled(False)
    else:
        ui.radioButton_2.setEnabled(True)
        ui.radioButton_3.setEnabled(True)

def StartPushButton():

    import GlobalVars
    
    ui.StartPushButton.setEnabled(False)
    ui.RescanInputsPushButton.setEnabled(False)
    ui.ThresholdLineEdit.setEnabled(False)
    ui.BirdNameLineEdit.setEnabled(False)
    ui.InputSelectioncomboBox.setEnabled(False)
    ui.WorkingDirpushButton.setEnabled(False)
    ui.BufferTimeSpinBox.setEnabled(False)
    ui.radioButton.setEnabled(False);
    ui.radioButton_2.setEnabled(False);
    ui.radioButton_3.setEnabled(False);    
    
    GlobalVars.isRunning=1

    TriggeredRecordAudio(ui)
    

def ThresholdLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.threshold=int(newvalue)

def radioButtonClicked():
      import GlobalVars
      print(str(GlobalVars.ThreshChan))
      GlobalVars.Stereo= not GlobalVars.Stereo # Set stereo, trigger on L/R
      if not GlobalVars.Stereo:
          #GlobalVars.ThreshChan=          # Set Mono, trigger on only channel
          ui.radioButton_2.setEnabled(False)
          ui.radioButton_3.setEnabled(False)
      else:
          ui.radioButton_2.setEnabled(True)
          ui.radioButton_3.setEnabled(True)
          

def radioButton_2Clicked(): #left
      import GlobalVars
      GlobalVars.ThreshChan='left'

def radioButton_3Clicked(): #right
    import GlobalVars  
    GlobalVars.ThreshChan='right'
    
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)
    
def InputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    
    GlobalVars.inputdeviceindex=int(newvalue)
    p = pyaudio.PyAudio()
    print(newvalue);
    #print(p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels'))
    
    if (p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels'))>1:
        ui.radioButton.setEnabled(True)
    else:
        ui.radioButton.setEnabled(False);

    p.terminate
  
def BirdNameLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.filename=str(newvalue)

def WorkingDirpushButtonClicked():
    import os
    import GlobalVars
    
    dialog = QtGui.QFileDialog()
    dialog.setFileMode(QtGui.QFileDialog.Directory)
    dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, True)
    
    directory = QtGui.QFileDialog.getExistingDirectory(dialog, 'Select Drive')
    directory = str(directory)
    print(directory)
    GlobalVars.path=directory+'/'
    

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        from numpy import arange, array, zeros
        import GlobalVars;
        
        GlobalVars.buffertime=1
        GlobalVars.threshold=50
        GlobalVars.filename='birdname'
        GlobalVars.inputdeviceindex=0
        GlobalVars.Stereo=False;
        GlobalVars.ThreshChan='left'
        GlobalVars.CHANNELS=1;
        GlobalVars.isRunning=False;


        self.RescanInputsPushButton.connect(self.RescanInputsPushButton,
                                                QtCore.SIGNAL(("clicked()")),
                                                RescanInputsButtonPushed)

        self.StopPushButton.connect(self.StopPushButton,
                                                QtCore.SIGNAL(("clicked()")),
                                                StopPushButton)

        self.StartPushButton.connect(self.StartPushButton,
                                                QtCore.SIGNAL(("clicked()")),
                                                StartPushButton)

        self.ThresholdLineEdit.connect(self.ThresholdLineEdit,
                                                QtCore.SIGNAL(("textChanged(QString)")),
                                                ThresholdLineEditChanged)

        self.BirdNameLineEdit.connect(self.BirdNameLineEdit,
                                                QtCore.SIGNAL(("textChanged(QString)")),
                                                BirdNameLineEditChanged)
                                               
        self.BufferTimeSpinBox.connect(self.BufferTimeSpinBox,
                                                QtCore.SIGNAL(("valueChanged(int)")),
                                                BufferTimeSpinBoxChanged) 

        self.InputSelectioncomboBox.connect(self.InputSelectioncomboBox,
                                                QtCore.SIGNAL(("valueChanged(int)")),
                                                InputSelectioncomboBoxChanged)        

        self.WorkingDirpushButton.connect(self.WorkingDirpushButton,
                                                QtCore.SIGNAL(("clicked()")),
                                                WorkingDirpushButtonClicked)
        #
        self.radioButton.connect(self.radioButton,
                                                QtCore.SIGNAL(("clicked()")),
                                                radioButtonClicked)
        self.radioButton_2.connect(self.radioButton_2,
                                                QtCore.SIGNAL(("clicked()")),
                                                radioButton_2Clicked)
        self.radioButton_3.connect(self.radioButton_3,
                                                QtCore.SIGNAL(("clicked()")),
                                                radioButton_3Clicked)

        self.radioButton_2.setEnabled(False)
        self.radioButton_3.setEnabled(False)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    RescanInputsButtonPushed()
    sys.exit(app.exec_())
    #window.show()
    sys.exit(app.exec_())


