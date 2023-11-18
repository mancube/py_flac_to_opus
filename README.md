![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

<img src='https://i.imgur.com/Dk1BtAg.png' width='150'></img>

# py_flac_to_opus
Audio converter for converting FLAC to OPUS files.
Written fully in Python, GUI done in TKinter.

---

## Features
- Converts FLAC files to OPUS files
- Handles batch folder conversions, with the option to remove source files
- Correctly copies over tags and album artwork, including the cover image (if existing)
- Works on Windows and Linux

---

## Requirements
Needs a **FFmpeg** install accessible, either via *PATH enviroment variables* or provide the **ffmpeg** executable *yourself* in the same folder as the source.

Here's a link to the [FFmpeg documentation](https://github.com/FFmpeg/FFmpeg) on GitHub, containing the explanation of the installation process.

---

## Installation
The installation is done via the **pip** package manager.

Necessary imports are listed in the requirements.txt file, can be installed via:
```
pip install -r requirements.txt
```

---

## Releases
The release contains a ZIP file with the Windows executable created via Pyinstaller.

The basic config.json config file gets generated on the first run of the program.

Can also be run from source code.

```
python gui.py
```

*~~If running the executable, the icon.ico is necessary in the root folder for the executable to run as intended.~~*

From the v1.1 version onward, the icon is provided via a different method, so the icon.ico isn't needed anymore.

---

## Screenshots
![Imgur](https://i.imgur.com/1ZoipHi.png)

The basic user interface, with the options to choose the input and output folders, for batch processing.

Using TKinter's TTK libraries for theming purposes.

---

## To-Do List
- [ ]  Add a preset import/export system
- [ ]  Add more audio formats (*big*)
- [ ]  Add seperate GUI settings, for configuring the program look and any additional features