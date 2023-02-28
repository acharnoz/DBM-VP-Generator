d# WOW-VoicePack-Generator

## Project resume

Python scripts to easily create Voice Packs for World of Warcraft addons. These scripts use AI audio engine to create voices from translated texts.

These scripts are provided by Milho, Dalaran EU Realm.

*Note: It's been a very long time since I've developed. This project is first and foremost a way for me to have a good time.*

## Project plans

* Develop some basic python scripts to provide a first version of a french voice pack for DBM
* Improve the french version for the wow retail version
* Provide a french voice pack for the wow classic version and wow tbc classic version
* Test different AI Audio Engines (Google, "Alexa", "Siri", "Watson", Windows, open source library, etc)
* Test different sound effects (Audio gain, speech speed, etc)
* Try collaborating with other DBM VoicePack contributors to collect correct translations and provide these translations to the wow community
* Develop a python script to direclty generate a complete DBM VoicePack from player custom texts
* Develop a python script to generate media voices to use with SharedMedia to use these sounds with DBM or another addons (eg Weak Aura).
* Develop tools to retrieve boss spells (from wow api ? wowhead api ?), the translation and generate dictionary for voice generation
* Develop a python web app (and publish it) to propose the DBM VoicePack generation online
* Develop a python web app (and publish it) to propose the media voices generation online
* Develop a python app or web app to allow users to directly register their voice to generate a voice package

## Project install

### Windows

* Install python 3 (https://www.python.org/downloads/windows/)
* Add the python bin in your PATH (e.g. on powershell $Env:PATH += ";C:\XXXXX)
* Install google AI voice engine 'pip install gtts'
* Install aws amazon AI voice engine 'pip install boto3'
* Install google translate engine 'pip install googletrans'
* Install pydub (manipulate audio with an simple and easy high level interface)
  * Download the windows release build of libdav on your computer (https://libav.org/download/ or http://builds.libav.org/windows/release-lgpl/)
  * Extract libdav and add the path 'XXX\libav\usr\bin' in your PATH (e.g. on powershell $Env:PATH += ";C:\XXXXX")
  * pip install pydub
  * $Env:PATH += ";G:\Dev\ffmpeg\bin"
  * $Env:PATH += ";G:\Dev\ffmpeg\bin;G:\Dev\bin\libav\usr\bin"

### Mac

TODO

### Linux

TODO

## Use of scripts

### General

> python.exe scritps/XXX.py -h

Print the script help

### Dictionary generation

> cmd-dico-create.py

Script to create an empty dictionary from .ogg files included in an addon folder.

> cmd-dico-translate.py

Script to translate a dictionary and export the result.

> cmd-dico-compare.py

Script to compare two dictionaries and print result.

> cmd-dico-merge.py

Script to merge two dictionaries and export the result.

### Ogg file generation

> cmd-oggfiles-create-voice.py

Script to create an ogg file from a text.

> cmd-oggfiles-create-voicepack.py

Script to create a voice pack from a dictionary.

> cmd-oggfiles-update-voicepack.py

Script to update a voice pack from dictionary differences.

## Project history

TODO


## Update audio files for DBM
> Copy DBM-VPEM files in DBM-VPVEM-REF
> python .\scripts\cmd-dico-create.py -l fr -n DBM-VPVEM-REF -o .\DBM-VPVEM-REF\DBM-VPVEM-REF.json .\DBM-VPVEM-REF
> python .\scripts\cmd-dico-compare.py .\DBM-VPVEM-REF\DBM-VPVEM-REF.json .\dbm-dictionaries\dbm-vp-fr.json
> python .\scripts\cmd-dico-merge.py .\dbm-dictionaries\dbm-vp-fr.json .\DBM-VPVEM-REF\DBM-VPVEM-REF.json -o .\dbm-dictionaries\new-dbm-vp-fr.json
> remove in dbm dictioannary "di.ogg": "DUMMY", "didi.ogg": "DUMMY",
> cmd-oggfiles-update-voicepack.py

> python scripts\cmd-oggfiles-update-voicepack.py -c .\my-audio-configs\aws-french-optimal-config.json .\dbm-dictionaries\dbm-vp-fr.json ..\DBM-VoicePack-FrenchFemale\DBM-VPFrenchFemale\dictionary.json -o .\test\ -e AWS
> copy generated file from test to ..\DBM-VoicePack-FrenchFemale\DBM-VPFrenchFemale\dictionary.json



## Update audio files for DBMEA
> python .\scripts\cmd-dico-create-gamedata.py (comment line to select game data generation)
> View generated files to G:\Dev\WOW-VoicePack-Generator\test\dbmea
> compare dico 
> python .\scripts\cmd-dico-compare.py .\test\dbmea\DBMEA-Party-WoD-FR.json ..\addons\DBMEA-Party-WoD-FR\dictionary.json
> copy lua et dico dans l'addon
> generate files
> python .\scripts\cmd-oggfiles-create-voicepack.py -e GTTS -c .\my-audio-configs\gtts-french-optimal-config.json ..\addons\DBMEA-Party-Dragonflight-FR\DBMEA-Party-Dragonflight-FR.json -o ..\addons\DBMEA-Party-Dragonflight-FR\

> python .\scripts\cmd-gamedata-explore.py -l en -dbp ..\WoWGameDataDB  -aid
> python .\scripts\cmd-gamedata-create-addon-DF.py -l fr --gamedatadbpath ..\WoWGameDataDB --addondbpath ..\DBMEventAnnouncement\DBMEA-FR-Voicepacks\
> python .\scripts\cmd-gamedata-create-addon-DF.py -l en --gamedatadbpath ..\WoWGameDataDB --addondbpath ..\DBMEventAnnouncement\DBMEA-EN-Voicepacks\    