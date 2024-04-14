- [MS Teams Busy Light](#ms-teams-busy-light)
- [Hardware](#hardware)
	- [Electronics](#electronics)
- [Software](#software)
	- [Installation as a User](#installation-as-a-user)
	- [Installation as a developer](#installation-as-a-developer)
		- [Installing Git](#installing-git)
		- [Installing Visual Studio Code and Extensions](#installing-visual-studio-code-and-extensions)
		- [Setup .venv in Visual Studio Code](#setup-venv-in-visual-studio-code)
		- [Create new .exe](#create-new-exe)
	- [How to get the presence status](#how-to-get-the-presence-status)
		- [MS Teams OLD](#ms-teams-old)
		- [MS Teams NEW](#ms-teams-new)
		- [Teams Presence status](#teams-presence-status)
- [Results and Assembly](#results-and-assembly)
	- [Assembly](#assembly)
	- [Results](#results)
- [Reference / Link Collection](#reference--link-collection)
# MS Teams Busy Light

Repository for a DIY Busy light, that should represents the Teams presence status in a small box, that will turn a plexiglass 
with indirect LED light into a matching presence color.


# Hardware

Disclaimer regarding the choice of Hardware: Although there is some hardware that would better fit for the purpose, 
I decided to use the following items, because I had (at least some of them) already in my drawer. 

* plexiglass sheet
* Arduino Nano (Chip: Atmel atmega328p Xplained mini)
* wood 
* WS2812 5050 RGB LEDs (Neopixel)

I created a CAD Modell of it, using Catia. Besides the Part Modell itself, I created the drawing of the plexiglass and 
wooden stand, as well as their PDF exports, so you don't need Catia to open them. Here you can see a first rendering of the model: 
![rendered](images/rendered.bmp)

## Electronics
Find the Wiring Diagram of the Neopixel RGB Strips and the Arduino below. They will fit to the bottom of the wooden stand. 
![wiring diagram](images/wiring%20diagram.png)

# Software

## Installation as a User

As a user you just need to download the latest version from [releases](https://github.com/MarcelSchm/MS-Teams-Busy-Light/releases) and run the .exe file. 

## Installation as a developer

If you want to participate in this development, you can check out the current state of development by

### Installing Git

open CMD or powershell and type:

	winget install -e --id Git.Git

```
git clone https://github.com/MarcelSchm/MS-Teams-Busy-Light.git <your-repopath>
```

### Installing Visual Studio Code and Extensions


open CMD or powershell and type:


	winget install -e --id Microsoft.VisualStudioCode


* Open Visual Studio Code.
* Select _Extensions_ in the side menu icons.
  * Search for _Python_ → Click Install.
  * Search for _Pip Manager_ → Click Install.
  * Search for _Markdown All in One_ → Click Install.
* Click _File_ → _Open Workspace from File_.
* Select _MS-Teams-Busy-Light.code-workspace_ from the repo path.
* Hit <kbd>Enter</kbd>.


### Setup .venv in Visual Studio Code

* Click <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> and enter ``Create Environment``.
* Select _Venv_ and hit <kbd>Enter</kbd>.
* Select _requirements.txt_ install _Venv_ with the needed pip libraries.

### Create new .exe

Just execute the the [Powershell Script](createNewTeamsBusyLightExe.ps1) in a powershell admin shell. 

## How to get the presence status

There are different ways of fetching the presence status of teams. Microsoft provides the status of your account that 
is used in Teams via the Graph API. This might come in handy for future versions of the busy light: 
instead of just having one Hardware that represents your status in one color, you can split the LED to actually also show 
the status of another colleague. Unfortunately, to access the Graph API, your organization needs to grant consent 
for the organization so everybody can read their Teams status. Since my organization didn't want to grant consent, 
I needed to find a workaround. If you might want to check it on your own hou can find some information on the documentation of
[how to get presence using Graph API][6].
One of them is the monitor the MS Teams log file on the local Harddrive.

> [!NOTE]
> This solution below only works for the OLD version of Microsoft Teams. The new version is on a different location, with some differences and limitations. Therefore, there will be an updated `MS-Teams-Settings.config` config setting file, that can be used to confige which version you want to use. 


### MS Teams OLD
The location of this file: 

	C:\Users\%userprofile%\AppData\Roaming\Microsoft\Teams\logs.txt
	
Idea on what/how to read from the log file I got from [this repository][2].

### MS Teams NEW
The location of this file: 

	C:\Users\%localappdata%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\Logs


	
### Teams Presence status
The Log File contains several information. 
Changes in Teams Presence status can be obtained from messages containing ```StatusIndicatorStateService: Added```, message containing information for Calls contain ```DeviceCallControlManager Desktop:```.
This is the List of possible Teams Status that are available:
(Main )

| StatusName in Teams | StatusName in Log File  |  				Color 					| Command String send to Arduino |
|:-------------------:|:-----------------------:|:-------------------------------------:|:------------------------------:|
|    Available        |        Available        | 	:green_heart: green :green_heart: 	|			Green				 |
|    Busy             |     Busy                | 	 :heart: red :heart:			    |			Red				 	 |
|    In a meeting     | InAMeeting  			|	 :heart: red :heart:			    |			Red				 	 |
|    In a call        |     OnThePhone          | 	 :heart: red :heart:			    |			Red				 	 |
|    Do not disturb   | DoNotDisturb ,Presenting| 	 :heart: red :heart:			    |			Red				 	 |
|    Be right back    |     BeRightBack         | :yellow_heart: yellow :yellow_heart:	|			Yellow				 |
| 	 Away             |		Away				| :yellow_heart: yellow :yellow_heart:	|			Yellow				 |
|	 Offline          |		Offline				| :yellow_heart: yellow :yellow_heart:	|			Yellow				 |
| 		N/A			  | NewActivity				| 						N/A	 			|								 |
| 		N/A			  | Unknown,ConnectionError,NoNetwork| :heart: red :heart:		 	|			Red				 	 |
| 	'Calling' Window  | reportIncomingCall 		| :heart: red :heart:		 			|			BlinkRed				 	 |


| Additional Status apart from Teams | 				Description 				  |  				Color 				  | Command String send to Arduino |
|:----------------------------------:|:------------------------------------------:|:-------------------------------------:|:------------------------------:|
|Established Connection				 | After successfully connecting to COM- Port | :white_heart: white :white_heart:	  |				White			   |
| Outdated 				| Status information in Log file is older than start of script| :green_heart: green :green_heart: |				Green		       |	


# Results and Assembly

## Assembly 
After creating the wooden stand, plexiglas and soldering of the electronics, you need to put everything together. should be selfexplaining, but here have a look of my assembly:
![assembly](images/assembly_and_glue.jpg)
You can see here, that I prepared to glue a thin layer of vaneer wood to the  backside, too cover the electronics. 

## Results
Here you can find some pictures of the current state / final version of the busy light:
![red_no_engrave](images/red_without_Engraving.jpg)
![green_no_engrave](images/green_without_engraving.jpg)
![red_engrave](images/red_with_engraving.jpg)
![green_engrave](images/green_with_engraving.jpg)


# Reference / Link Collection

I gathered the above information from various sources. Here to find the link collection, everything not directly linked above
was just added to this file for the complete Link list, I used for inspiration, even if it was not used at the end. 


[1]: <https://www.reddit.com/r/MicrosoftTeams/comments/iuxcac/diy_busylight/?rdt=45645> "Reddit Discussion"
[2]: <https://github.com/ajobbins/AHK-Teams-Presence> "AutoHotKey Log"
[3]: <https://github.com/JnyJny/busylight> 
[4]: <https://github.com/toblum/ESPTeamsPresence>
[5]: <https://www.eliostruyf.com/diy-building-busy-light-show-microsoft-teams-presence/>
[6]: <https://learn.microsoft.com/en-us/graph/api/presence-get?view=graph-rest-beta&tabs=http#code-try-1>
[7]: <https://www.hackster.io/benedikt-hubschen/office-busylight-1a8e30>
[8]: <https://teamsqueen.com/2021/08/19/a-busylight-with-microsoft-teams/>
[9]: <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>





