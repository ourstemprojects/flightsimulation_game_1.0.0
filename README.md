
<h1>Application Overview</h1>
The Digital Engine Simulator application is controlled via the Queue Manager and Dashboard applications

<h1>Launching the Application</h1>
The following steps are to be carried out on the Raspberry Pi.
To launch the Digital Engine Simulator application, simply double-click the Launch Pi.sh icon on the Desktop.  When prompted click on “Execute”.
If this does not work correctly, then you can launch the application from the command prompt by typing:-
<br>
cd ~/des_profilegenerator
<br>
sudo python digitalenginesimulator.py digitalenginesimulator.cfg
<br>

<h1>Application Operation</h1>
Once invoked, the application will wait until a player is selected for play.
A player is selected for play using the Queue Manager and Dashboard Applications
To start the game for a selected player, the player must press the “START” button on the handlebars of the bike.
The game will run for 90 seconds.  When complete, the player’s score is displayed for 10 seconds, the program resets and waits for the next player.

Function keys are used to control the behaviour of the application.
ESC = Exit the application and close.

<h1>Software Design</h1>

<a href="digitalenginesimulator.png" target="_blank"><img src="digitalenginesimulator.png" alt="profile generator design" style="max-width:100%;"></a></p>
