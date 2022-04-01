# PyCBS
 Python version of CBS (Catch Bird Singing) for single audio card.



 Simple Python (3.6) based verson of the old CBS program.  Plots RMS of audio input, lets you choose sound devices, can be run  concurrently, and records in mono or stereo .WAV format, can be triggered off L/R channels if necessary for,, e.g., TAF or other strange triggers if you prefer. 

Requires: 

PyAudio
https://people.csail.mit.edu/hubert/pyaudio/

But in case you want to use more channels later, install the one from:

	https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
	
	with ALSA support. 

from pip, you can install

pyqt5
pyqtgraph


From the original documentation of the orignal CBS (Catch Bird Singing, by David Perkel), 

"Also, I am not a programmer, so I don't want to hear complaints.  I know it
isn't written well.  However, I would love to hear suggestions, even things
that may seem obvious."
