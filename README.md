# CognitiveTask

## Cognitive Cycling ITF project

* Uses Python 3.6.10 (Anaconda 3 4.4.0) on Windows 10 64-bit
* Needs video codec to play videos; recommends [K-Lite Codec Pack Basic](https://codecguide.com/download_k-lite_codec_pack_basic.htm)
* Requires installation of libant-master/libant-master/setup.py, go to folder and type `python setup.py install` into anaconda prompt with admin permissions
* Other bits and bobs to install see error when running it; `pyserial`, `pyglet`, `pynput`, `nidaqmx`, `psychopy --no-deps`
* Videos not included in commit, in .mp4 format under the \Videos folder or C:\Data\Videos; change it in VideoPlayer.py
* Usage with controller/keyboard/touchscreen/mouse; controller recommended
* DAQ, Encoder and Pedal data saves out to C:\Data folder as .csv file.[DAQ at 1000Hz for 100 samples, Encoder slaved to DAQ at 10Hz, and Pedal Data at 1Hz]

## Hardware

1. Dell Optiplex 7060
2. TP-Link UH700 USB 3.0 7-Port USB Hub
3. USB Gaming Controller (optional but recommended)
4. Absolute Optical Encoder connected using RS232 Serial port (COM5)
5. PowerTap P1 power meter using an ANT+ USB stick
6. Polar H10 heart rate sensor band using also ANT+ USB stick
7. EMG on ai0-3 on USB-6001 DAQ (Dev1)
8. PPG on ai4 on USB-6001 DAQ (Dev1)
9. Ability to connect to EEG PC using DB25 USB2LPT Parallel Port converter using psychopy. [Taobao Link](https://item.taobao.com/item.htm?spm=a1z09.2.0.0.595a2e8d7JkFOT&id=19835544254&_u=e2n4hf9r63a1)
    * Using "Debug register trap" will cause BSOD 0x109 on Windows 10.

## Currently 5 tasks are implemented

1. Erikssen Flanker Task ``Task 0``
2. Recall Task (Verbal) ``Task 1``
3. Recall Task (Visuospatial)  ``Task 2``
4. n-back Task (Verbal) ``Task 3``
5. n-back Task (Visuospatial) ``Task 4``
6. Majority Task ``Task 5``
7. Stroop Task ``Task 6``

## Steps to install

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
    6. `pip install pywinusb`
7. install libant at libant-master/libant-master/ with: `python setup.py install`
8. Ensure that you can import from python: `from PyQt5 import QtMultimediaWidgets`
    1. `pip uninstall PyQt5`
    2. `pip uninstall PyQt5-sip`
    3. `pip install PyQt5-sip`
    4. `pip install PyQt5`
9. Download the [USB2LPT converter driver](https://www-user.tu-chemnitz.de/~heha/basteln/PC/USB2LPT/index.en.htm), direct the unknown device in device manager to the downloaded file and under the `/en` folder
10. In order to use Parallel port to communicate, you require the `inpout**.dll(Windows version dependent)` files in the same folder as your .py files. Link to .dll binaries [here](http://www.highrez.co.uk/downloads/inpout32/)
11. Find `h#s USB to LPT converter` in Device Manager. Ensure that the `h#s USB to LPT converter` in Device Manager is `LPT2`:

    * Emulation Tab:
        * Emulated port address: `278h(632,LPT2)`
        * LPT enchancement mode: `SPP`
        * Select `Debug register trap`
    * Port Settings Tab:
        * Select `Never use an interrupt`
        * Select `Enable legacy Plug and Play dection`
        * LPT Port Number: `LPT2`

## Troubleshooting

* ```[Errno None] b'libusb0-dll:err [_usb_reap_async] reaping request failed, win error: A device attached to the system is not functioning.\r\n\n'```
  * unplug and replug the ANT+ USB stick

* Blue Screen of Death (BSOD)
  * Incompatibility of USB2LPT drivers with Win10, will need replacement possibly with arduino.

## WARNING

* Modify xinput3_KeyboardControll_NES_Shooter_addGameTask.py for xinput vesion when changing between Win10, Win 8/7 and WinVista

## Parallel Port output command legend (0-255)

| Flanker Task          |   |
|-----------------------|---|
|"Flanks Shown"         |10 | CNV Preparedness
|"Question Shown-Con"   |11 |
|"Question Shown-Incon" |12 |
|"User Answered Correct"|15 |
|"User Answered Wrong"  |16 |

| Working Memory-Verb   |20 |
|-----------------------|---|
|"Question Shown"       |21 |
|"Answers Shown"        |23 |
|"User Answered Correct"|25 |
|"User Answered Wrong"  |26 |

| Working Memory-Space |30 |
|----------------------|---|
|"Question Shown"      |31 |
|"Answers Shown"        |33 |
|"User Answered Correct"|35 |
|"User Answered Wrong"  |36 |

| n-back-Verb           |   |
|-----------------------|---|
|"Task n-1"             |41 |
|"Task n-2"             |42 |
|"Task n-3"             |43 |
|"Question Shown-True"  |49 |
|"Question Shown-False" |48 |

| n-back-Space          |   |
|-----------------------|---|
|"Task n-1"             |51 |
|"Task n-2"             |52 |
|"Task n-3"             |53 |
|"Question Shown-True"  |59 |
|"Question Shown-False" |58 |

| Majority               |60 |
|------------------------|---|
|"Answers/Question Shown"|4  |
