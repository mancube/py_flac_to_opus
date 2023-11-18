![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

<img src='https://i.imgur.com/Dk1BtAg.png' width='150'></img>

# py_flac_to_opus
Audio converter for converting FLAC to OPUS files.
Written fully in Python, GUI done in TKinter.

## Requirements
Needs a **FFmpeg** install accessible, either via *PATH enviroment variables* or provide the **ffmpeg** executable *yourself* in the same folder as the source.

Here's a link to the [FFmpeg documentation](https://github.com/FFmpeg/FFmpeg) on GitHub, containing the explanation of the installation process.

## Installation
The installation is done via the **pip** package manager.

Necessary imports are listed in the requirements.txt file, can be installed via:
```
pip install -r requirements.txt
```

## Releases
The release contains a zip file with the executable created via Pyinstaller, and the basic config.json file.

Can also be run from source code.

```
python gui.py
```

~~If running the executable, the icon.ico is necessary in the root folder for the executable to run as intended.~~

From the v1.1 version onward, the icon is provided via a different method, so the icon.ico isn't needed anymore.

## Screenshots
![Imgur](https://i.imgur.com/1ZoipHi.png)

The basic user interface, with the options to choose the input and output folders, for batch processing.

Using TKinter's TTK libraries for theming purposes.
