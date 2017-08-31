
# Application Overview
The Digital Engine Simulator application is controlled via the Scoreboard application

# Launching the Application
The following steps are to be carried out on the Raspberry Pi.
To launch the Digital Engine Simulator application, simply double-click the Launch Pi.sh icon on the Desktop.  When prompted click on “Execute”.
If this does not work correctly, then you can launch the application from the command prompt by typing:-
<br>
> cd ~/des_profilegenerator
<br>
> sudo python digitalenginesimulator.py digitalenginesimulator.cfg
<br>

# Application Operation
Once invoked, the application will wait until a player is selected for play.
A player is selected for play using the Scoreboard application
To start the game for a selected player, the player must press the “START” button on the handlebars of the bike.
The game will run for 90 seconds.  When complete, the player’s score is displayed for 10 seconds, the program resets and waits for the next player.

Function keys are used to control the behaviour of the application.
ESC = Exit the application and close.

# Software Design

<a href="digitalenginesimulator.png" target="_blank"><img src="digitalenginesimulator.png" alt="profile generator design" style="max-width:100%;"></a></p>
