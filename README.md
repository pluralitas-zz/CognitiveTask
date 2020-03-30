# CognitiveTask
 Cognitive Cycling ITF project

* Uses Python 3.6.10 (Anaconda 4.3.0) on Windows 10 64bit
* Needs video codec to play videos; recommends k-lite codec pack basic https://codecguide.com/download_k-lite_codec_pack_basic.htm
* Requires installation of libant-master/libant-master/setup.py, go to folder and type "python setup.py install" into anaconda prompt with admin permissions
* Other bits and bobs to install see error when running it; pyserial, pyglet, pynput, nidaqmx, "psychopy --no-deps"
* Videos not included in commit, in .mp4 format under the \Videos folder.
* Usage with controller/keyboard/touchscreen/mouse; controller recommended
* DAQ, Encoder and Pedal data saves out to C:\Data folder as .csv file.[DAQ at 1000Hz for 100 samples, Encoder slaved to DAQ at 10Hz, and Pedal Data at 1Hz]

Hardware:
1. USB Controller (optional but recommended)
2. Absolute Optical Encoder connected using RS232 Serial port (COM6)
3. PowerTap P1 power meter using an ANT+ USB stick
4. Elecrow Easy Pulse v1.1 for PPG connected using Digital Output to ai0 on USB-6001 DAQ
5. EMG on ai1-4 on USB-6001 DAQ (Dev1)
6. Ability to connect to EEG PC using DB25 Parallel port type using psychopy.parallel library

Currently 4 tasks are implemented:
1. Erikssen Flanker Task
2. Verbal Recall Task (Visuospatial, Verbal)
3. Visual Recall Task (Visuospatial, Verbal)
4. n-back Task

WARNING
* Modify xinput3_KeyboardControll_NES_Shooter_addGameTask.py for xinput vesion when changing between Win10, Win 8/7 and WinVista
