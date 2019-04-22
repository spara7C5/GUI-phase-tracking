# GUI-phase-tracking

## What is it? 
GUI-phase-tracking is a Graphical User Interface Software which supports the development of a new system for the polarization-insensitive 
phase recovery of the signal transmitted via optical fiber in a frequency metrology dissemination setup.
The system is based on a DSP algorithm which elaborates the four signals of a dual-polarization optical hybrid (DPOH).
The outputs obtained by the algorithm are the optical phase `PH` and the two birefringence parameters of the optical fiber `DE` and `TH`.



## Getting Started



### OS Prerequisites

#### Linux-like

* Python (>=3)

* Tkinter (tested on 8.6
	To install tkinter you should use your package manager:
    * Debian:
    
    ```
    apt-get install python3-tk
    ```
    
    * openSUSE
    
    ```
    zypper in python3-tk
    ```
    * To install on other OS (E.G. mac, Windows) refers to:
    
    	[tkdocs.com/tutorial/install.html](https://tkdocs.com/tutorial/install.html)

* NumPy & SciPy python modules

```
pip3 install numpy scipy
```

* NumExpr python module (tested on version 2.6.8)

```
pip3 install numexpr 
```

* matplotlib python module

```
pip3 install matplotlib
```
**ACHTUNG!** Make sure  your `python` command is a symbolic link to `Python3` (not to `python2`).

You can easily check running:

```
ls -l $(which python)
```
if it is not, you HAVE to fix the aliases on .bashrc or run this software with:

```
python3 GUI_phase.py
```
#### Windows-like

The software fully runs out of the box on Win10 in a IDE such as Anaconda/Spyder.<br />
Follow the above linux-like section for running in CMD console.<br />
A dedicated installer for a standalone running is on the way....

## Running 

Press the green button "Clone or Download" at the project home page in the github website.<br />
Download the zip, if you want to run the software.<br />
Clone the repo if you want to develop and version it.<br />

#### Linux-like

Open a terminal and go to the GUI-phase-tracking directory.

Next launch `GUI_phase.py`

```
python GUI_phase.py
```
#### Windows-like

Extract the zip and play `GUI_phase.py` with the IDE

## Instructions for use

### LOAD TAB

This tab is in charge of load the four lists of sampled values of the DPOH channels. It can be done by two way:<br />
The `Load from file` section manages a file (txt,csv,...) of collected experimental data. It must be formatted in five columns respectively
 |relative time|chx-real|chx-imag|chy-real|chx-imag| with a certain Delimiter which must be specified in the corresponding text box.
Other DSP pre-processing features are available: chunking, downsampling, mixing for demodulation.
The `Load from simulated data` offers the possibility to simulate the transmission system, namely the behavior of the optical fiber with the
DE e TE parameters and the optical (demodulated) phase PH.
**NOTE!** the equations in the textbox must be written following the python/matlab syntax and the independent variable must be called `x` and 
it must be always present (e.g. a simple constant K is written as 0*x+K )

### CHANNELS TAB

This section visualizes the four electric channels. Additional whitenoise can be added for simulation purposes as well as a low pass filter.
In case you want to go back, simply uncheck from the unwanted checkbox and press again the REFRESH button

### CHANNELS TAB

This tab computes the phase noise PSD of each channel using a single-photodiode phase detection method.
It should be used for short data collection where the channels have constant module or for a quick estimation of the harmonics affecting 
the electronic channels.

### RECOVERY TAB

In this tab the recovery algorithm is performed by pressing the *Track* button.
It can take several minutes, during which the GUI is blocked.<br />
In addition the tab provides the phase PSD of the retrieved phase and the phase residual (the last one is computed only for simulated data)

## Built With

* [SYMPY](https://docs.sympy.org/latest/index.html) - Symbolic calculation library
* [PAGE](http://page.sourceforge.net/) - Python Automatic GUI Generator
* [NUMPY](http://www.numpy.org/) - Package for scientific computing with Python
* [NUMEXPR](https://github.com/pydata/numexpr) - Fast numerical expression evaluator for NumPy

## Authors

* [**Stefano PARAcchino**](https://github.com/spara7C5) - *Initial work* and main developer
* [**Federico Bassignana**](https://github.com/JustMe011) - Consultant, troublesolver, implementer of experimental branches

