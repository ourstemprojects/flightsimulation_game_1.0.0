#!/usr/bin/python
try:
    import sys
    from Tkinter import *
    import tkMessageBox
    import Tkinter as ttk
    from ttk import *
    import random
    import time
    import MySQLdb
    import ConfigParser
except Exception, e:
    print("FATAL: import error: %s" % str(e))
    exit(0)
#endtry    
 
root = Tk()
root.title("Avatar Selection Application")

# read the config file into the object
config = ConfigParser.ConfigParser()
  
# Create a Tkinter variable
tkcolorvar = StringVar(root)
tkanimalvar = StringVar(root)
tkplacesvar = StringVar(root)
tknumbervar = StringVar(root)

# Dictionary with options
color_choices = ["-","White","Silver","Gray","Black","Navy","Blue","Cerulean","Blue","Turquoise","Green","Azure","Teal","Cyan","Yellow","Lime","Chartreuse" ]
tkcolorvar.set(color_choices[0])

animal_choices = ["-", "Fox","Coyote","Tiger","Lynx","Octopus","Penguin","Skunk","Monkey","Starfish","Hamster","Snail","Tortoise","Toucan","Donkey" ]
tkanimalvar.set(animal_choices[0])

places_choices = ["-", "Alpha","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliet","Kilo","Lima","Mike","November","Oscar","Papa","Quebec","Romeo","Sierra","Tango","Uniform","Victor","Whiskey","X-Ray","Yankee","Zulu" ]
tkplacesvar.set(places_choices[0])

number_choices = ["-", random.randint(10, 19), random.randint(20, 29), random.randint(30, 39), random.randint(40, 49), random.randint(50, 59), random.randint(60, 69), random.randint(70, 79), random.randint(80, 89), random.randint(90, 99) ]
tknumbervar.set(number_choices[0])

def createavatar_callback():

    try:

        # read the db configuration elements from the filename
        hostname=config.get('databaseconnection', 'hostname')
        username=config.get('databaseconnection', 'username')
        password=config.get('databaseconnection', 'password')
        dbname=config.get('databaseconnection', 'dbname')
        tablename=config.get('databaseconnection', 'avatartablename')

        print "createavatar_callback(): hostname=%s; username=%s; password=%s; dbname=%s; tablename=%s" % (hostname,username,password,dbname,tablename)

        if tkcolorvar.get() == "-" or tkanimalvar.get() == "-" or tkplacesvar.get() == "-" or tknumbervar.get() == "-":
            # warn the user they need to complete everything
            tkMessageBox.showinfo("Avatar Selection", "Sorry, you need to select a colour, animal, place and number")
        else:
            #create the connection to the database
            db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
            #create a cursor for the select
            cur = db.cursor()

            # format the avatar name
            thechoosenavatar = "%s%s%s%s" % (tkcolorvar.get(), tkanimalvar.get(), tkplacesvar.get(), tknumbervar.get())
            
            # create a new row in the database and commit
            sqlcommandstr = "INSERT INTO %s.%s (name,status,datecreated,gamehighscore,queueposition) VALUES ('%s','QUEUED','%s', %d, %d)" % (dbname, tablename, thechoosenavatar, time.strftime('%Y-%m-%d %H:%M:%S'),0,time.time())
            print "createavatar_callback(): sqlcommandstr=%s" % sqlcommandstr
            cur.execute(sqlcommandstr)
            db.commit()

            # close the cursor
            cur.close()

            # close the connection
            db.close()

            # declare success and reset the form
            tkMessageBox.showinfo("Avatar Selection", "An avatar named '%s' has been created and added to the queue, please wait to be called.  Thank-you." % thechoosenavatar)
            startagain_callback()
        #endif
    #endtry        
    except Exception, e:
        print("createavatar_callback(): error %s" % str(e))
        tkMessageBox.showinfo("Avatar Selection", "Unable to create the desired Avatar, please ask for assistance")
    #endexcept
    finally:
        pass
    #endfinally            
    
#enddef

def startagain_callback():
    try:
        tkcolorvar.set(color_choices[0])
        tkanimalvar.set(animal_choices[0])
        tkplacesvar.set(places_choices[0])
        tknumbervar.set(number_choices[0])
        print "createavatar_callback(): choices reset"
    #endtry        
    except Exception, e:
        print("startagain_callback(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally        
#enddef

#
#
# the purpose of this function is the entry point for the software, it loads config varialbles, starts pygame and GPIO before invoking the main loop
def main(configfilename):

    try:

        # Add a grid
        mainframe = Frame(root)
        mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        mainframe.columnconfigure(0, weight = 1)
        mainframe.rowconfigure(0, weight = 1)
        mainframe.pack(pady = 10, padx = 10)

        # read the configuration file
        config.read(configfilename)
         
        color_popupMenu = OptionMenu(mainframe, tkcolorvar, *color_choices)
        Label(mainframe, text="Choose a color").grid(row = 1, column = 1)
        color_popupMenu.grid(row = 1, column =2)

        animal_popupMenu = OptionMenu(mainframe, tkanimalvar, *animal_choices)
        Label(mainframe, text="Choose an animal").grid(row = 2, column = 1)
        animal_popupMenu.grid(row = 2, column =2)

        word_popupMenu = OptionMenu(mainframe, tkplacesvar, *places_choices)
        Label(mainframe, text="Choose a word").grid(row = 3, column = 1)
        word_popupMenu.grid(row = 3, column =2)

        number_popupMenu = OptionMenu(mainframe, tknumbervar, *number_choices)
        Label(mainframe, text="Choose a number").grid(row = 4, column = 1)
        number_popupMenu.grid(row = 4, column =2)

        startagain_button = Button(mainframe, text="Start Again", command=startagain_callback)
        startagain_button.grid(row = 5, column =1)

        createavatar_button = Button(mainframe, text="Create Avatar", command=createavatar_callback)
        createavatar_button.grid(row = 5, column =3)

        root.mainloop()
    #endtry        
    except Exception, e:
        print("main(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally
        
#enddef

#
#
# the purpose of this is to allow the application to be invoked from the commandline and pass sys.argv[1] into main()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("ERROR: You must specify the configuration filename on the command line")
        exit(1)
    else:
        # get the config name from the command line and pass in
        main(sys.argv[1])
    #endif
#endif

#EOF
