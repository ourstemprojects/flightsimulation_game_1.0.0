#!/usr/bin/python
try:
    import sys
    from pygame import *
    import pygame
    import time
    import os
    import random
    import ConfigParser
    import MySQLdb
except Exception, e:
    print("FATAL: import error: %s" % str(e))
    exit(0)
#endtry    

# system wide constants
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
BANNERHEIGHT = 200

# create the config parser object and Font for text display
config = ConfigParser.ConfigParser()
Font = None

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)
        f.close()
    #endwith
#endef

#
#
# the purpose of this function is to load and image (thefile) and return as a surface
def load_image(thefile):
    # loads an image, prepares it for play    
    try:
        print ("load_image(): loading image")
        thefile = os.path.join(os.path.dirname(sys.argv[0]), "", thefile)
        surface = pygame.image.load(thefile)
    #endtry
    except pygame.error:
        print("load_image(): Could not load image! [thefile=%s errcode=%s]" % (thefile, pygame.get_error()))
    #endexcept
    return surface.convert()
#enddef

#
#
# the purpose of this function is to display a bsnner (thebannerimagefilename) and bsckground image (thebackgroundimagefilename) over the entire screen (hWnd)
def display_background(hWnd, thebannerimagefilename, thebackgroundimagefilename):

    try:

        print ("display_background(): loading background images")
        
        # load the banner
        theimage = load_image(thebannerimagefilename)
        hWnd.blit( theimage, (0, 0) )
        display.flip()

        # load the background
        theimage = load_image(thebackgroundimagefilename)
        hWnd.blit( theimage, (0, BANNERHEIGHT) )
        display.flip()
    #endtry        
    except Exception, e:
        print("display_background(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally                
#enddef

#
#
# the purpose of this function is to display the queue of avatars waiting to play
def display_queuemanager(hWnd):
    try:
        print ("display_queuemanager(): drawing queuemanager")

        # read the db configuration elements from the filename
        hostname=config.get('databaseconnection', 'hostname')
        username=config.get('databaseconnection', 'username')
        password=config.get('databaseconnection', 'password')
        dbname=config.get('databaseconnection', 'dbname')
        tablename=config.get('databaseconnection', 'avatartablename')

        print "display_queuemanager(): hostname=%s; username=%s; password=%s; dbname=%s; tablename=%s" % (hostname,username,password,dbname,tablename)

        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT status,rownum,name,datecreated,gamehighscore,queueposition,avatar FROM %s.%s WHERE status <> 'COMPLETE' ORDER BY queueposition ASC" % (dbname, tablename)
        print "display_queuemanager(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        rowtop=BANNERHEIGHT

        hWnd.blit(Font.render(
            "|%05s|%08s|%26s|" % ("order", "status", "name"),
            1, (155, 155, 155), (0,0,0)), (2, rowtop)
        )

        rowtop += 20
        queueorder=1
        
        # paint the data
        for row in cur.fetchall():
            #data from rows
            status = str(row[0])
            rownum = str(row[1])
            name = str(row[2])
            datecreated=str(row[3])
            gamehighscore=long(row[4])
            queueposition=long(row[5])

            # get the image data and dump out to file
            imagedata = row[6]
            filename = "%s.png" % name
            write_file(imagedata, filename)

            # resize and dar onto the svreen
            theimage = load_image(filename)
            theimage = pygame.transform.scale(theimage, (16,16) )
            hWnd.blit( theimage, (450, rowtop) )
            display.flip()

            # delete the file
            os.remove(filename)
            
            hWnd.blit(Font.render(
                "|%05d|%08s|%26s|" % (queueorder, status, name),
                1, (155, 155, 155), (0,0,0)), (2, rowtop)
            )

            rowtop += 20
            queueorder += 1

            display.flip()
        #endfor
            
        # close the cursor
        cur.close()

        # close the connection
        db.close()
    #endtry        
    except Exception, e:
        print("display_queuemanager(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally                       
#enddef

def send_player_to_end_of_queue():
    try:

        print ("send_player_to_end_of_queue(): sending top player to end of the queue")

        # read the db configuration elements from the filename
        hostname=config.get('databaseconnection', 'hostname')
        username=config.get('databaseconnection', 'username')
        password=config.get('databaseconnection', 'password')
        dbname=config.get('databaseconnection', 'dbname')
        tablename=config.get('databaseconnection', 'avatartablename')

        print "send_player_to_end_of_queue(): hostname=%s; username=%s; password=%s; dbname=%s; tablename=%s" % (hostname,username,password,dbname,tablename)

        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT status,rownum FROM %s.%s WHERE status = 'QUEUED' ORDER BY queueposition ASC LIMIT 1" % (dbname, tablename)
        print "send_player_to_end_of_queue(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        # grab the important details from the record (should only be one)
        for row in cur.fetchall():
            status = str(row[0])
            rownum = str(row[1])
        #endfor

        # update the queueposition to current time which will force the player to the bottom
        sqlcommandstr = "UPDATE %s.%s SET queueposition = '%d' WHERE rownum = '%s'" % (dbname, tablename, time.time(), rownum)
        print"send_player_to_end_of_queue(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)
        db.commit()

        # close the cursor
        cur.close()

        # close the connection
        db.close()
    #endtry        
    except Exception, e:
        print("send_player_to_end_of_queue(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally                     
#enddef

def select_player_for_game():
    try:

        print ("select_player_for_game(): selecting top player for the game")

        # read the db configuration elements from the filename
        hostname=config.get('databaseconnection', 'hostname')
        username=config.get('databaseconnection', 'username')
        password=config.get('databaseconnection', 'password')
        dbname=config.get('databaseconnection', 'dbname')
        tablename=config.get('databaseconnection', 'avatartablename')

        print "select_player_for_game(): hostname=%s; username=%s; password=%s; dbname=%s; tablename=%s" % (hostname,username,password,dbname,tablename)

        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT status,rownum FROM %s.%s WHERE status = 'QUEUED' ORDER BY queueposition ASC LIMIT 1" % (dbname, tablename)
        print "select_player_for_game(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        # grab the important details from the record (should only be one)
        for row in cur.fetchall():
            status = str(row[0])
            rownum = str(row[1])
        #endfor

        sqlcommandstr = "UPDATE %s.%s SET status = 'PLAYING' WHERE rownum = '%s'" % (dbname, tablename, rownum)
        print "select_player_for_game(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        # commit the update
        db.commit()

        # close the cursor
        cur.close()

        # close the connection
        db.close()
    #endtry        
    except Exception, e:
        print("select_player_for_game(): error %s" % str(e))
    #endexcept
    finally:
        pass
    #endfinally                             
#enddef

#
#
#
def display_scoreboard(hWnd):
    try:
        print ("display_scoreboard(): drawing scoreboard")

        # read the db configuration elements from the filename
        hostname=config.get('databaseconnection', 'hostname')
        username=config.get('databaseconnection', 'username')
        password=config.get('databaseconnection', 'password')
        dbname=config.get('databaseconnection', 'dbname')
        tablename=config.get('databaseconnection', 'avatartablename')

        print "display_scoreboard(): hostname=%s; username=%s; password=%s; dbname=%s; tablename=%s" % (hostname,username,password,dbname,tablename)

        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT rownum,name,datecreated,gamehighscore,queueposition FROM %s.%s WHERE status = 'COMPLETE' ORDER BY gamehighscore DESC" % (dbname, tablename)
        print "display_scoreboard(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)


        rowtop=BANNERHEIGHT

        hWnd.blit(Font.render(
            "|%04s|%26s|%07s|" % ("rank", "name", "hiscore"),
            1, (255, 255, 255), (0,0,0)), (450, rowtop)
        )

        rowtop += 20
        ranking=1
        
        # paint the data
        for row in cur.fetchall():
            #data from rows
            rownum = str(row[0])
            name = str(row[1])
            datecreated=str(row[2])
            gamehighscore=long(row[3])
            queueposition=long(row[4])
            
            hWnd.blit(Font.render(
                "|%04d|%26s|%07d|" % (ranking, name, gamehighscore),
                1, (255, 255, 255), (0,0,0)), (450, rowtop)
            )

            rowtop += 20
            ranking+= 1

            display.flip()
        #endfor
            
        # close the cursor
        cur.close()

        # close the connection
        db.close()
    except Exception, e:
        print("display_scoreboard(): error %s" % str(e))
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

        print ("main(): program start")

        # read the config file into the object
        config.read(configfilename)

        # read the application variables
        windowcaption = config.get('general', 'windowcaption')
        backgroundimagefilename = config.get('general', 'backgroundimagefilename')
        bannerimagefilename = config.get('general', 'bannerimagefilename')

        # debug print
        print ("main(): windowcaption=%s" % windowcaption)
        print ("main(): backgroundimagefilename=%s" % backgroundimagefilename)
        print ("main(): bannerimagefilename=%s" % bannerimagefilename)

        # init pygame, set the size and caption
        pygame.init()
        win = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT + BANNERHEIGHT))
        display.set_caption("Queue Manager and Scoreboard: " + windowcaption)

        # Set the font sizes
        global Font
        Font = font.SysFont("ubuntumono", 20, bold=False, italic=False)

        # display banner and background screen
        display_background(win, bannerimagefilename, backgroundimagefilename)

        # Main application loop
        going = True
        while going:
            for e in event.get():

                # Red X to exit
                if e.type == QUIT:
                    going = False
                #endif

                # keypress handlers
                if e.type == KEYDOWN:
                    
                    # ESC to quit
                    if e.key == K_ESCAPE:
                        print ("main(): Esc pressed exiting")
                        going = False
                    #endif

                    # F1 select the top avatar in the queue to play the game
                    elif e.key == K_F1:
                        print ("main(): F1 pressed player selected")
                        select_player_for_game()
                    #endif

                    # F2 send the top avatar in the queue to the end of the queue
                    elif e.key == K_F2:
                        print ("main(): F2 pressed top player send to bottom")
                        send_player_to_end_of_queue()
                    #endif
                        
                    elif e.key == K_DELETE:
                        print ("main(): DELETE pressed top player removed from queue")
                    #endif

                #endif
            #endfor

            # paint the queue manager and scoreboard
            win.fill(Color(0, 0, 0), (0, BANNERHEIGHT, win.get_width(), win.get_height()))
            display_queuemanager(win)
            display_scoreboard(win)

            # loop delay to preserve CPU
            time.sleep(1)
            
        #endwhile

        # tidy yp pygame and GPIO and release
        pygame.quit()

        print ("main(): program end")
        
        return
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
        
