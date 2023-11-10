<img src='logo.png' width='150'></img>
# py_flac_to_opus
Audio converter for converting FLAC to OPUS files.
Written in Python, GUI done in Tkinter.

# Requirements
Needs a <b>ffmpeg</b> install accessible via PATH enviroment variables.

Needed imports are listed in the requirements.txt file, can be installed via:
```
pip install -r requirements.txt
```

# Releases
The release contains a zip file with the executable created via Pyinstaller, and the basic config.json file.

Can also be run from source code.

```
python gui.py
```

If running the executable, the icon.ico is necessary in the root folder for the executable to run as intended.

# Screenshots
![Imgur](https://i.imgur.com/zunc6to.png)

The basic user interface, with the options to choose the input and output folders, for batch processing.

Using Tkinter's TTK libraries for theming purposes.
