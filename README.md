# win_tts
Synthèses vocale oobabooga

"Win TTS" is a text-to-speech extension for Oobabooga. It offers text-to-speech functionality to enrich the user experience within the Oobabooga environment.

![Mon Image](https://drive.google.com/uc?export=view&id=1X0Pn-0P7h7RrxB5bOU_xHdqgxQbCyLy5)

## Table des matières

- [Installation](#installation)
- [Functionality](#functionality)
- [Bonus](#bonus)

## Installation

Now clone this repository in the extensions folder :
```bash
git clone https://github.com/tijo95/win_tts.git
```

Install pyttsx4 library
```bash
pip install -r requirements.txt
```

## Functionality

Activation and deactivation: The extension allows users to activate or deactivate text-to-speech according to their needs.

Automatic playback: Users can choose to have the audio file played back automatically.

Text Display: The extension also offers the option of displaying text or not, in addition to the generated audio.

Live TTS: Users can activate real-time text-to-speech, allowing a voice synthesizer to read the text as it is typed "once the wav audio recording is deactivated".

Customizable parameters: The extension offers customizable parameters, such as speech speed, volume and system voice selection.

Save TTS Outputs: The extension lets you save settings.

remove wav directory: removes all wav files from the directory. 

## Bonus

under windows11* some "fr" voices are not in the right system directory to be detected they can be moved easily from the registry , For "fr" voices I put you the registry file to run directly .

for other languages "en", "es" ... I'll show you what to do if you have unavailable voices after running the extensions.

Here is a summary of the steps I followed. It assumes that you already have downloaded the voice packs .

1- Open ```regedit.exe``` (Windows + R, and type regedit) and navigate to the Registry key ```Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens```.

2- Right click on the voice you want to use and chose export.

3- Open the exported file with a text editor (for example Notepad++).

4- Copy all the text a second time in the file so you have everything two times (except the first line ```Windows Registry Editor Version 5.00```).

5- In the first part of the data, replace ```\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens``` by ```HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens``` (you have to do this at two distinct places).

6- In the second part (the one you pasted below), do the same but change for ```HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens``` (again, two places to change).

7- Save the file, close it, and double click it. Accept the registry modification.

8- Restart your computer.

Now the exported voices are available to use with pyttsx4!
