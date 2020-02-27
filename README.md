# CognitiveTask
 Cognitive Cycling ITF

* Uses Python 3.6 (Anaconda 4.3.0) on Windows 10
* Needs ffmpeg codec, recommends k-lite codec pack basic https://codecguide.com/download_k-lite_codec_pack_basic.htm
* Requires installation of libant-master/libant-master/setup.py by typing "python setup.py install" into anaconda prompt
* Other bits and bobs to install see error when running it.
* Videos not included in commit
* Usage with controller/keyboard/touchscreen/mouse

Hardware:
1. USB Controller (optional)
2. Absolute Optical Encoder connected using RS232 Serial port
3. PowerTap P1 power meter using an ANT+ USB stick
4. Easy Pulse v1.1 for PPG connected using ai0 on USB-6001 DAQ
5. EMG on ai1-4 on USB-6001 DAQ

Currently 4 tasks are implemented:
1. Erikssen Flanker Task
2. Verbal Recall Task
3. Visual Recall Task
4. n-back Task

