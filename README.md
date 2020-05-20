# CognitiveTask

## Cognitive Cycling ITF project:

* Uses Python 3.6.10 (Anaconda 3 4.4.0) on Windows 10 64-bit
* Needs video codec to play videos; recommends [K-Lite Codec Pack Basic](https://codecguide.com/download_k-lite_codec_pack_basic.htm)
* Requires installation of libant-master/libant-master/setup.py, go to folder and type `python setup.py install` into anaconda prompt with admin permissions
* Other bits and bobs to install see error when running it; `pyserial`, `pyglet`, `pynput`, `nidaqmx`, `psychopy --no-deps`
* Videos not included in commit, in .mp4 format under the \Videos folder or C:\Data\Videos; change it in VideoPlayer.py
* Usage with controller/keyboard/touchscreen/mouse; controller recommended
* DAQ, Encoder and Pedal data saves out to C:\Data folder as .csv file.[DAQ at 1000Hz for 100 samples, Encoder slaved to DAQ at 10Hz, and Pedal Data at 1Hz]

## Hardware:

1. Dell Optiplex 7060
2. TP-Link UH700 USB 3.0 7-Port USB Hub
3. USB Controller (optional but recommended)
4. Absolute Optical Encoder connected using RS232 Serial port (COM6)
5. PowerTap P1 power meter using an ANT+ USB stick
6. Elecrow Easy Pulse v1.1 for PPG connected using Digital Output to ai4 on USB-6001 DAQ (Dev1)
7. EMG on ai0-3 on USB-6001 DAQ (Dev1)
8. Ability to connect to EEG PC using DB25 Parallel port type using psychopy.parallel library

## Currently 5 tasks are implemented:

1. Erikssen Flanker Task
2. Verbal Recall Task (Visuospatial)
3. Verbal Recall Task (Verbal)
4. n-back Task (Visuospatial)
5. n-back Task (Verbal)
6. Divided Attention Task (able to fake other tasks)

## Steps to install anaconda and python

1. Install [Anaconda 3 4.4.0 64-bit](https://repo.anaconda.com/archive/Anaconda3-4.4.0-Windows-x86_64.exe)
2. `conda update conda -y`
3. `conda install tqdm=4.19 -y`
4. `conda update anaconda -y`
5. Ensure Python version is 3.6.10: `python -V`
6. use pip to install packages needed to run program: 
    1. `pip install pyserial`
    2. `pip install pyglet`
    3. `pip install pynput`
    4. `pip install nidaqmx`
    5. `pip install psychopy --no-deps`
7. install libant at libant-master/libant-master/ with: `python setup.py install`
8. Ensure that you can import from python: `from PyQt5 import QtMultimediaWidgets`
    1. `pip uninstall PyQt5`
    2. `pip uninstall PyQt5-sip`
    3. `pip install PyQt5-sip`
    4. `pip install PyQt5`

## Troubleshooting
* ```[Errno None] b'libusb0-dll:err [_usb_reap_async] reaping request failed, win error: A device attached to the system is not functioning.\r\n\n' ```
    * unplug and replug the ANT+ USB stick

* ```unsupported operand type(s) for -: 'str' and 'int'```
    * yet to solve

## WARNING

* Modify xinput3_KeyboardControll_NES_Shooter_addGameTask.py for xinput vesion when changing between Win10, Win 8/7 and WinVista
