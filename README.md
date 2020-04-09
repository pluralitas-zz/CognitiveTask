# CognitiveTask
 Cognitive Cycling ITF project

* Uses Python 3.6.10 (Anaconda 4.4.0) on Windows 10 64bit
* Needs video codec to play videos; recommends k-lite codec pack basic https://codecguide.com/download_k-lite_codec_pack_basic.htm
* Requires installation of libant-master/libant-master/setup.py, go to folder and type "python setup.py install" into anaconda prompt with admin permissions
* Other bits and bobs to install see error when running it; pyserial, pyglet, pynput, nidaqmx, "psychopy --no-deps"
* Videos not included in commit, in .mp4 format under the \Videos folder or C:\Data\Videos; change it in VideoPlayer.py
* Usage with controller/keyboard/touchscreen/mouse; controller recommended
* DAQ, Encoder and Pedal data saves out to C:\Data folder as .csv file.[DAQ at 1000Hz for 100 samples, Encoder slaved to DAQ at 10Hz, and Pedal Data at 1Hz]

Hardware:
1. Dell Optiplex 7060
2. TP-Link UH700 USB 3.0 7-Port USB Hub
3. USB Controller (optional but recommended)
4. Absolute Optical Encoder connected using RS232 Serial port (COM6)
5. PowerTap P1 power meter using an ANT+ USB stick
6. Elecrow Easy Pulse v1.1 for PPG connected using Digital Output to ai0 on USB-6001 DAQ
7. EMG on ai1-4 on USB-6001 DAQ (Dev1)
8. Ability to connect to EEG PC using DB25 Parallel port type using psychopy.parallel library

Currently 4 tasks are implemented:
1. Erikssen Flanker Task
2. Verbal Recall Task (Visuospatial, Verbal)
3. Visual Recall Task (Visuospatial, Verbal)
4. n-back Task

Steps to install anaconda and python
1. Install Anaconda 4.4.0 64-bit
2. "conda update conda -y"
3. "conda install tqdm=4.19 -y"
4. "conda update anaconda -y"
5. use pip to install packages needed to run program

WARNING
* Modify xinput3_KeyboardControll_NES_Shooter_addGameTask.py for xinput vesion when changing between Win10, Win 8/7 and WinVista
