# CognitiveTask

## Cognitive Cycling ITF project

* Uses Python 3.6.9 (Anaconda 3 2019.10) on Windows 10 64-bit
* Usage with controller/keyboard/touchscreen/mouse; controller recommended
* DAQ, Encoder and Pedal data saves out to C:\Data folder as .csv file.[DAQ at 1000Hz for 100 samples, Encoder slaved to DAQ at 10Hz, and Pedal Data at 1Hz]

## Hardware

1. Dell Optiplex 7060 running Windows 10 64-bit
2. TP-Link UH700 USB 3.0 7-Port USB Hub
3. USB Gaming Controller (optional but recommended)
4. Absolute Optical Encoder connected using RS232 Serial port (COM5)
5. PowerTap P1 power meter using an ANT+ USB stick
6. Polar H10 heart rate sensor band using also ANT+ USB stick
7. EMG on ai0-3 on USB-6001 DAQ (Dev1)
8. PPG on ai4 on USB-6001 DAQ (Dev1)
9. Ability to connect to EEG PC using [PCIe Parallel Port with card](https://hken.rs-online.com/web/p/serial-boards/1383754)

## Prerequistes for operation
1. Install "FESCycling" installer for NI MAX and DAQ drivers.
2. Set DAQ to "Dev1" in NI MAX
3. Check that "ANT USBstick2" does not have error(Yellow Exclamation) in Device Manager, else direct Windows to the drivers in the zip package.
4. Install [Visual Studio Code](https://code.visualstudio.com/download) with [Code Runner](https://marketplace.visualstudio.com/items?itemName=formulahendry.code-runner) extension for display and editing the codes
5. Install video codec to play videos; recommends [K-Lite Codec Pack Basic](https://codecguide.com/download_k-lite_codec_pack_basic.htm)

## Steps to install for experiment

1. Download the code as zip package. REMEMBER to check that the branch is `master` for experiment. Unzip the package into a folder
2. Install [Anaconda 3 2019.10 64-bit](https://repo.anaconda.com/archive/Anaconda3-2019.10-Windows-x86_64.exe)
3. Ensure Python version is 3.6.9: `python -V`
4. Use pip to install packages needed to run program by typing this in `Anaconda Prompt`: 
    * `pip install pyserial pyglet pynput nidaqmx pywinusb psychopy --no-deps`
5. Install libant by accessing `"code folder"/libant-master/libant-master/` using `Anaconda Prompt` with: `python setup.py install`
6. Ensure that you can import from python: `from PyQt5 import QtMultimediaWidgets`, else:
    1. `pip uninstall PyQt5`
    2. `pip uninstall PyQt5-sip`
    3. `pip install PyQt5-sip`
    4. `pip install PyQt5`
7. Add the relevant videos into `C:/Data/Videos` folder for background videos

## Install for EEG

1. Download the code as zip. REMEMBER to check that the branch is `EEGOnly` for experiment.
2. Install as per steps for experiment
3. Access `writeout.py` and change the parallel port address to your hardware, you may use the parallel port tester included in the zip package.

## Running the program

1. Open the folder in Visual Studio Code.
2. Ensure that the VS Code detects the python version installed on the bottom left corner.
3. Open `main.py`
4. Change the `UserIDNAME` to the subject's ID
5. Run by clicking on the Play button on the top right and selecting "Run in Terminal"

## Troubleshooting

* ```[Errno None] b'libusb0-dll:err [_usb_reap_async] reaping request failed, win error: A device attached to the system is not functioning.\r\n\n'```
  * unplug and replug the ANT+ USB stick

## Others

* Modify xinput3_KeyboardControll_NES_Shooter_addGameTask.py for xinput vesion when changing between Win10, Win 8/7 and WinVista

## Currently 5 tasks are implemented

1. Erikssen Flanker Task ``Task 0``
2. Recall Task (Verbal) ``Task 1``
3. Recall Task (Visuospatial)  ``Task 2``
4. n-back Task (Verbal) ``Task 3``
5. n-back Task (Visuospatial) ``Task 4``
6. Majority Task ``Task 5``
7. Stroop Task ``Task 6``

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
