from PyQt5 import QtCore, QtGui, uic, QtWidgets


import pyaudio 
import wave
import audioop
from collections import deque
import os
import time
import math
import GlobalVars
import copy
global graph_win
from numpy import arange, true_divide
import array
import pyqtgraph as pg

import pdb

#import pyqtgraph.exporters




CHUNK = 8192 # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)s
RATE = 44100# sampling frequency
MAX_DUR=60 #max dur in seconds

def RescanInputs():
    import GlobalVars

   
    inputdevices = 0
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            print("DevID ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
            inputdevices+=1

    GlobalVars.numdevices=inputdevices
    p.terminate()


def TriggeredRecordAudio(ui):

 import GlobalVars
 global graph_win
 
 MIN_DUR=GlobalVars.buffertime*2+0.1;
 #isRunning 

 threshold=GlobalVars.threshold;
 SILENCE_LIMIT = GlobalVars.buffertime;
 PREV_AUDIO = GlobalVars.buffertime;

 p = pyaudio.PyAudio()

 GlobalVars.CHANNELS=1;
       
 
 stream=p.open(format=FORMAT,input_device_index=GlobalVars.inputdeviceindex,channels=GlobalVars.CHANNELS,rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)

    
 ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
 audio2send = []
 
 #cur_data = '' # current chunk of audio data
 rel = int(RATE/CHUNK)
 slid_win = deque(maxlen=SILENCE_LIMIT * rel) #amplitude threshold running buffer
 prev_audio = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 perm_win = deque(maxlen=PREV_AUDIO*rel)
 
 data = b''.join(list(perm_win))
 plotarray = array.array("i",data); 
     
 started = False
 cur_data=stream.read(CHUNK)
 

 def updateGraph():
        
         t=arange(plotarray.buffer_info()[1])
         t=true_divide(t, RATE)
         ui.GraphWidget.plot(t,plotarray, width=1, clear=True)

 timer = pg.QtCore.QTimer()
 timer.timeout.connect(updateGraph)
 timer.start(100)
 
 count=1;
 
 while (GlobalVars.isRunning==1):
  
  cur_data = stream.read(CHUNK)  
  count=count+1
  if (count>5):
      count=0
      QtWidgets.qApp.processEvents()

  slid_win.append(cur_data) #(audioop.rms(cur_data, 2))

  perm_win.append(cur_data)  
  data = b''.join(list(perm_win))

  if (pyaudio.get_sample_size(FORMAT)==2):
      plotarray = array.array("h",data);  # force 16 bit, since that's the correct #
  else:
      plotarray=  array.array("i",data);  # not 16 bit, so.... 
      
 

  if(sum([x > GlobalVars.threshold for x in plotarray])>0 and len(audio2send)<MAX_DUR*rel):    
   if(not started):
    ui.ListeningTextBox.setText('<span style="color:red">singing</span>')
    started = True
   audio2send.append(cur_data)
  elif (started is True and len(audio2send)>MIN_DUR*rel):
   print("Finished")
   filename = save_audio(list(prev_audio) + audio2send) #,GlobalVars.path,GlobalVars.filename)
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)
   prev_audio = copy.copy(perm_win)
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
   audio2send=[]
  elif (started is True):
   ui.ListeningTextBox.setText('too short')
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)
   prev_audio = copy.copy(perm_win)
   audio2send=[]
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
  else:
   prev_audio.append(cur_data)
   
 print("done recording")
 stream.close()
 p.terminate()

def save_audio(data):
 import GlobalVars
    
 """ Saves mic data to  WAV file. Returns filename of saved
 file """
# filename = GlobalVars.path+'_'+str(int(time.time()))
 # writes data to WAV file
 T=time.localtime()
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 filename = GlobalVars.filename+'_'+outtime
 rootdir=GlobalVars.path;
 DatePath='/'+str("%02d"%T[0])+'_'+str("%02d"%T[1])+'_'+str("%02d"%T[2])+'/' 
 filename = rootdir+DatePath+filename+'_'+outtime

 
 if not os.path.exists(os.path.dirname(rootdir+DatePath)):
    try:
        os.makedirs(os.path.dirname(rootdir+DatePath))
    except:
        print('File error- bad directory?')

 data = b''.join(data)
 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(GlobalVars.CHANNELS);
 wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
 wf.setframerate(RATE) 
 wf.writeframes(data)
 wf.close()
 return filename + '.wav'
 

##
##if(__name__ == '__main__'):
## audio_int()
## record_song()

