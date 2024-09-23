# Suite.st Autoclicker

Autoclicking tool supporting work in QA TV LAB and allowing for typing in complex text on any device.

## Introduction

Program that translates strings into set of remote inputs that can write out given string onto the devices available in the QA TV LAB. The program itself produces a string that contains the list of commands that can be coppied into a test in suite.st. If program runs on MacOs it will copy the commands into the clipboard, otherwise the string has to be coppied from the console where it will be printed. The command list will be changed based on the platform that the commands are prepared for.

## Usage

```
python main.py <platform> <string>
```

\<platform\> indicates which keyboard layout should be used, and \<string\> contains data that should be inputed on the device. For example:

```
python main.py sagemcom Test-String
```

The above instruction will prepare "Test-String" using sagemcom platform.
Currently available platforms can be checked using

```
python main.py -h
```

and it should present a similar message (this one is coppied at the time of creation of this document):

```
usage: Suitest Autoclicker [-h] {sky,sagemcom,webos} string

Translates strings to clicks on remote to input them on the device

positional arguments:
  {sky,sagemcom,webos}  Platform of the device.
  string                Text that should be translated.

options:
  -h, --help            show this help message and exit
```

## Data

All the .json files can be found in the keyboards folder, they are hand made by observing the keyboards and their behaviours on the actual devices and compiling the applicable list of commands and their results.

## TODO

Saveguards while reading the file.
