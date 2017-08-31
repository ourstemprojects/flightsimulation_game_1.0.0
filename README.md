
## Application Overview
The Digital Engine Simulator application is controlled primarily via the Scoreboard application

# Launching the Application
The following steps are to be carried out on the Raspberry Pi.
To launch the Digital Engine Simulator application, simply double-click the Launch Pi.sh icon on the Desktop.  When prompted click on “Execute”.
If this does not work correctly, then you can launch the application from the command prompt by typing:-<br>
> cd ~/des_profilegenerator <br>
> sudo python digitalenginesimulator.py digitalenginesimulator.cfg <br> <br>
> Note: sudo is required as root access is needed to access the GPIO 

# Application Operation
The application will wait until a player is selected for play by the Dashboard application.
Once a player has been selected for play the target profile is drawn, the player name and avatar is image is displayed and the player is prompted to press the START button on the handlebars to continue.
A five second countdown is displayed, then the game starts.
The player must peddle the cycle for 90 seconds trying to match the target profile drawn, their actual speed is shown along with an aircraft icon.
At the end of the 90 seconds the game ends as their score is displayed for 10 seconds.  The game then return to idle move waiting for the next player.
The ESC key is used to exit the application and close when it is waiting for a player.

# Software Design

<a href="digitalenginesimulator.png" target="_blank"><img src="digitalenginesimulator.png" alt="profile generator design" style="max-width:100%;"></a></p>

# Technology Stack
Python 2.7.12<br>
GPIO python library<br>
pygame python library 1.91<br>
MySQLlib python library 1.37<br>
