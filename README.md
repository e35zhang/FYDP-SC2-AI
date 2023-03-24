## General Information
Artificial Intelligence using [sharpy-sc2](https://github.com/DrInfy/sharpy-sc2/wiki) and [python-sc2](https://github.com/BurnySc2/python-sc2) for playing [Starcraft 2](https://starcraft2.com/en-us/) using [sc2 api](https://github.com/Blizzard/s2client-api).

## Environment Setup
Clone this repo https://github.com/e35zhang/FYDP-SC2-AI.git

Install StarCraftII https://starcraft2.com/en-us/

install python 3.7.8

Run `pip install -r requirements.txt`

Copy the Maps folder in this project to the root folder of StarcraftII

## To run the bot vs ingame ai
`python run_custom.py -m EverDreamLE -p1 protossbot -p2 ai`

`python run_custom.py -m EverDreamLE -p1 protossbot -p2 protossbot`

`python run_custom.py -p1 human.protoss -p2 protossbot --map EverDreamLE `

Replays and logs will be in `games` folder.

## To publish the bots for ladder
to publish the bot(s) as ladder ready versions:
`python ladder_zip.py [botname]`

To publish the bot(s) as stand-alone executable:
`python ladder_zip.py [botname] -e`

published bot(s) will be in `publish` folder

## To get coding assistance in PyCharm
Mark sharpy-sc2 and sharpy-sc2/python directories as source roots.

## Documentation 
Refer to [design documentation](https://github.com/e35zhang/FYDP-SC2-AI/wiki) for overview.
Refer to [Project Report](https://github.com/e35zhang/FYDP-SC2-AI/blob/main/Project_Report.pdf) for detailed design.
