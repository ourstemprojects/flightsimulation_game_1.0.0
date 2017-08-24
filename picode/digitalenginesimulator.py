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
    import RPi.GPIO as g
#endtry
    
except Exception, e:
    if str(e) == "No module named RPi.GPIO":
        print "loading testRPiGPIO instead of RPi.GPIO"
        import testRPiGPIO as g
    else:
        print str(e)
        exit(0)
    #endif
#endtry

# system wide constants
WINDOWHEIGHT = 400
BANNERHEIGHT = 100
SINGLEPULSEBARHEIGHT = 20
PROGRESSBARHEIGHT = 6
MAXSAMPLEVALUE = 20

# Setup the configuration parser and fomt
config = ConfigParser.ConfigParser()
Font = None

# setup the scope of the pulse counter variable
global revcount
revcount = 0

# constants for the banner display function
WAIT_KEY = "key"
WAIT_GPIO = "gpio"
WAIT_DELAY = "delay"
DISPLAY_IMG = "img"
DISPLAY_TXT = "txt"

# signal completion of global code
print "global code in %s: complete" % sys.argv[0]

#
#
# the purpose of this function is to dump the data to a disc filename as a binary image
def write_file(data, filename):
    try:

        print "write_file(): data=%s" % data
        print "write_file(): filename=%s" % filename
        
        with open(filename, 'wb') as f:
            f.write(data)
            f.close()
        #endwith
    #endtry

    except Exception, e:
        print("write_file(): error '%s'" % str(e))
    #endexcept        

#endef

#
#
# the purpose of this function is to load and image (thefile) and return as a surface
def load_image(thefile):
    
    # loads an image, prepares it for play
    try:
        
        print "load_image(): thefile=%s" % thefile
        
        thefile = os.path.join(os.path.dirname(sys.argv[0]), "", thefile)
        surface = pygame.image.load(thefile)
    #endtry

    except pygame.error:
        print("load_image(): Could not load image '%s' errcode '%s'" % (thefile, pygame.get_error()))
    #endexcept

    return surface.convert()
#enddef

#
#
# the purpose of this function is to display the player name on the screen aong with thr avatar
def display_player_name(hWnd, theavatarname, y, thefontbackcolour, thefontforecolour):

    try:

        print "display_player_name(): hWnd=%s" % hWnd
        print "display_player_name(): theavatarname=%s" % theavatarname
        print "display_player_name(): y=%s" % y
        print "display_player_name(): thefontbackcolour=%s" % thefontbackcolour
        print "display_player_name(): thefontforecolour=%s" % thefontforecolour

        # generate the font text
        theavatarnameimage = Font.render("[%s] is now playing " % theavatarname, 1, (int(thefontforecolour[0]), int(thefontforecolour[1]), int(thefontforecolour[2])), (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])))
        print "display_player_name(): font.render(theavatarname)"

        # load the avatar image
        theavatarimage = load_image("%s.png" % theavatarname)
        theavatarimage = pygame.transform.scale(theavatarimage, (48,48) )
        print "display_player_name(): load_image(theavatarname)"
        
        print "theavatarnameimage.get_height()=%d" % theavatarnameimage.get_height()
        print "theavatarnameimage.get_width()=%d" % theavatarnameimage.get_width()
        print "theavatarimage.get_height()=%d" % theavatarimage.get_height()
        print "theavatarimage.get_width()=%d" % theavatarimage.get_width()

        # put the theavatarnameimage, theavatarimage and theimage onto the screen
        x = 0
        x = (hWnd.get_width() / 2) - (theavatarimage.get_width() / 2) - (theavatarnameimage.get_width() / 2)
        left = x - 3
        top = y - 3
        width = theavatarimage.get_width() + theavatarnameimage.get_width() + 6
        height = theavatarimage.get_height() + 6        
        pygame.draw.rect ( hWnd, (int(thefontforecolour[0]),int(thefontforecolour[1]),int(thefontforecolour[2])), Rect(left, top, width, height), 0)
        pygame.draw.rect ( hWnd, (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])), Rect(left+1, top+1, width-2, height-2), 0)
        hWnd.blit ( theavatarnameimage, (x , y  + (theavatarimage.get_height() / 2) - (theavatarnameimage.get_height() / 2) ) )    
        hWnd.blit ( theavatarimage, (x + theavatarnameimage.get_width(), y ) )        
        display.flip()

        print "display_player_name(): x=%d, y=%d" % (x, y)
        print "display_player_name(): top=%d, left=%d, width=%d, height=%d" % (top, left, width, height)
        
    #endtry

    except Exception, e:
        print("display_player_name(): error '%s'" % str(e))
    #endexcept
#enddef

#
#
# the purpose of this function is to display text on the screen along with the player name and avatar
def display_text_and_wait(hWnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thetextmessage, thewaitdelay, thegpiopin):

    try:

        print "display_text_and_wait(): hWnd=%s" % hWnd
        print "display_text_and_wait(): thegpio=%s" % thegpio
        print "display_text_and_wait(): theavatarname=%s" % theavatarname
        print "display_text_and_wait(): thefontbackcolour=%s" % thefontbackcolour
        print "display_text_and_wait(): thefontforecolour=%s" % thefontforecolour
        print "display_text_and_wait(): thetextmessage=%s" % thetextmessage
        print "display_text_and_wait(): thewaitdelay=%s" % thewaitdelay
        print "display_text_and_wait(): thegpiopin=%s" % thegpiopin

        # save screen to be restored at end
        wincopy = hWnd.copy()        

        # generate the font text
        theavatarnameimage = Font.render("[%s] %s" % (theavatarname, thetextmessage) , 1, (int(thefontforecolour[0]), int(thefontforecolour[1]), int(thefontforecolour[2])), (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])))
        
        # load the avatar image
        theavatarimage = load_image("%s.png" % theavatarname)
        theavatarimage = pygame.transform.scale(theavatarimage, (64,64) )

        # calculate X and Y required to put the avatar and message in the centre of the screen
        x = (hWnd.get_width() / 2) - (theavatarnameimage.get_width() / 2) - (theavatarimage.get_width() / 2)
        y = (hWnd.get_height() / 2) - (theavatarnameimage.get_height() / 2) - (theavatarimage.get_height() / 2) 

        # put the theavatarnameimage, theavatarimage onto the screen
        left = x - 3
        top = y - 3
        width = theavatarimage.get_width() + theavatarnameimage.get_width() + 6
        height = theavatarimage.get_height() + 6
        pygame.draw.rect ( hWnd, (int(thefontforecolour[0]),int(thefontforecolour[1]),int(thefontforecolour[2])), Rect(left, top, width, height), 0)
        pygame.draw.rect ( hWnd, (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])), Rect(left+1, top+1, width-2, height-2), 0)
        hWnd.blit ( theavatarnameimage, (x , y  + (theavatarimage.get_height() / 2) - (theavatarnameimage.get_height() / 2) ) )
        hWnd.blit ( theavatarimage, (x + theavatarnameimage.get_width(), y ) )
        display.flip()

        print "display_text_and_wait(): x=%d, y=%d" % (x, y)
        print "display_text_and_wait(): top=%d, left=%d, width=%d, height=%d" % (top, left, width, height)
        
        # if the wait delay is not zero then wait for the time, else if the GPOI pin is not zero then wait for it to go low
        if (thewaitdelay != 0):

            print "display_text_and_wait(): waiting for %d seconds" % thewaitdelay
            time.sleep(thewaitdelay)
            
        else:

            if (thegpiopin != 0):

                print "display_text_and_wait(): waiting for GPIO[%d] pin to go logic 0" % thegpiopin
                
                # Wait for the GPIO pin to toggle low button to be pushed
                start = True
                while start == True:
                    start = thegpio.input(thegpiopin)            
                    time.sleep(0.1)
                #while
            #endif
        #endif

        # restore the captured image from before
        hWnd.blit(wincopy, (0, 0))
        display.flip()        
        
    #endtry

    except Exception, e:
        print("display_text_and_wait(): error '%s'" % str(e))
    #endexcept
#enddef

#
# the purpose of this function is to display and image (thefilename) omto the window (hWnd)
# then either wait for the time specified (thewaitdelay) or until the (thegpio.thegpiopin) is pressed
def display_image_and_wait(hWnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, theimagefilename, thewaitdelay, thegpiopin):

    try:

        print "display_image_and_wait(): hWnd=%s" % str(hWnd)
        print "display_image_and_wait(): thegpio=%s" % str(thegpio)
        print "display_image_and_wait(): theavatarname=%s" % str(theavatarname)
        print "display_image_and_wait(): thefontbackcolour=%s" % str(thefontbackcolour)
        print "display_image_and_wait(): thefontforecolour=%s" % str(thefontforecolour)
        print "display_image_and_wait(): theimagefilename=%s" % str(theimagefilename)
        print "display_image_and_wait(): thewaitdelay=%s" % str(thewaitdelay)
        print "display_image_and_wait(): thegpiopin=%s" % str(thegpiopin)
        
        # save screen to be restored at end
        wincopy = hWnd.copy()

        # generate the font text
        theavatarnameimage = Font.render("[%s] " % theavatarname, 1, (int(thefontforecolour[0]), int(thefontforecolour[1]), int(thefontforecolour[2])), (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])))
        print "display_image_and_wait(): font.render(theavatarname)"
        
        # load the avatar image
        theavatarimage = load_image("%s.png" % theavatarname)
        theavatarimage = pygame.transform.scale(theavatarimage, (64,64) )
        print "display_image_and_wait(): load_image(theavatarname)"

        # load the overlay image and calculate the X and Y position
        theimage = load_image(theimagefilename)
        x = (hWnd.get_width() / 2) - (theimage.get_width() / 2)
        y = (hWnd.get_height() / 2) - (theimage.get_height() / 2)        

        print "display_image_and_wait(): x=%d, y=%d" % (x, y)        
        print "display_image_and_wait(): theavatarnameimage.get_height()=%d" % theavatarnameimage.get_height()
        print "display_image_and_wait(): theavatarnameimage.get_width()=%d" % theavatarnameimage.get_width()
        print "display_image_and_wait(): theavatarimage.get_height()=%d" % theavatarimage.get_height()
        print "display_image_and_wait(): theavatarimage.get_width()=%d" % theavatarimage.get_width()

        left = x - 3
        top = y - 3
        width = theavatarimage.get_width() + theavatarnameimage.get_width() + 6
        height = theavatarimage.get_height() + 6
        pygame.draw.rect ( hWnd, (int(thefontforecolour[0]),int(thefontforecolour[1]),int(thefontforecolour[2])), Rect(left, top, width, height), 0)
        pygame.draw.rect ( hWnd, (int(thefontbackcolour[0]),int(thefontbackcolour[1]),int(thefontbackcolour[2])), Rect(left+1, top+1, width-2, height-2), 0)
        hWnd.blit ( theavatarimage, (x , y  + (theavatarimage.get_height() / 2) - (theavatarimage.get_height() / 2) ) )
        hWnd.blit ( theimage, ( x, y ) )      
        display.flip()

        print "display_image_and_wait(): x=%d, y=%d" % (x, y)
        print "display_image_and_wait(): top=%d, left=%d, width=%d, height=%d" % (top, left, width, height)
        print "display_image_and_wait(): loaded '%s' and '%s.png'" % (thefilename, theavatarname)

        # if the wait delay is not zero then wait for the time, else if the GPOI pin is not zero then wait for it to go low
        if (thewaitdelay != 0):

            print "display_image_and_wait(): waiting for %d seconds" % thewaitdelay
            time.sleep(thewaitdelay)
            
        else:

            if (thegpiopin != 0):

                print "display_image_and_wait(): waiting for GPIO[%d] pin to go logic 0" % thegpiopin
                
                # Wait for the GPIO pin to toggle low button to be pushed
                start = True
                while start == True:
                    start = thegpio.input(thegpiopin)            
                    time.sleep(0.1)
                #while
            #endif
        #endif

        # restore the captured image from before
        hWnd.blit(wincopy, (0, 0))
        display.flip()
    #endtry

    except Exception, e:
        print("display_image_and_wait(): error '%s'" % str(e))
    #endexcept
    
#enddef

def display_item_then_wait(thehwnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thedisplaytype, thedisplayitem, thewaittype, thewaititem):

    try:

        print "display_item_then_wait(): thehwnd=%s" % str(thehwnd)
        print "display_item_then_wait(): thegpio=%s" % str(thegpio)
        print "display_item_then_wait(): theavatarname=%s" % str(theavatarname)
        print "display_item_then_wait(): thedisplaytype=%s" % str(thedisplaytype)
        print "display_item_then_wait(): thedisplayitem=%s" % str(thedisplayitem)
        print "display_item_then_wait(): thewaittype=%s" % str(thewaittype)
        print "display_item_then_wait(): thefontbackcolour=%s" % str(thefontbackcolour)
        print "display_item_then_wait(): thefontforecolour=%s" % str(thefontforecolour)
            
        if thedisplaytype == DISPLAY_IMG:

            if thewaittype == WAIT_GPIO:
                print "display_item_then_wait(): display_image_and_wait(hWnd, thegpio, thefilename, 0, thewaititem, theavatarname)"
                display_image_and_wait(thehwnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thefilename, 0, thewaititem)
            #endif

            if thewaittype == WAIT_DELAY:
                print "display_item_then_wait(): display_image_and_wait(hWnd, thegpio, thefilename, thewaititem, 0, theavatarname)"
                display_image_and_wait(thehwnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thefilename, thewaititem, 0)
            #endif
            
        #endif

        if thedisplaytype == DISPLAY_TXT:
            if thewaittype == WAIT_DELAY:
                print "display_item_then_wait(): display_text_and_wait(hWnd, theavatarname, thedisplayitem, thewaititem, 0)"
                display_text_and_wait(thehwnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thedisplayitem, thewaititem, 0)
            #endif
                
            if thewaittype == WAIT_GPIO:
                print "display_item_then_wait(): display_text_and_wait(hWnd, thegpio, theavatarname, thetextmessage, 0, thewaititem)"
                display_text_and_wait(thehwnd, thegpio, theavatarname, thefontbackcolour, thefontforecolour, thedisplayitem, 0, thewaititem)
                #exit(0)
            #endif
        #endif
    #endtry

    except Exception, e:
        print("display_item_then_wait(): error '%s'" % str(e))
    #endexcept        
                
#enddef

#
#
# the purpose of this function is to display a banner (thebannerimagefilename) and bsckground image (thebackgroundimagefilename) over the entire screen (hWnd)
def display_background(thehwnd, thebannerimagefilename, thebackgroundimagefilename):

    print "display_background(): thehwnd=%s" % thehwnd
    print "display_background(): thebannerimagefilename=%s" % thebannerimagefilename
    print "display_background(): thebackgroundimagefilename=%s" % thebackgroundimagefilename

    try:

        # load the banner
        theimage = load_image(thebannerimagefilename)
        pygame.transform.scale(theimage, (thehwnd.get_width(),BANNERHEIGHT) )
        thehwnd.blit( theimage, (0, 0) )
        display.flip()

        # load the background
        theimage = load_image(thebackgroundimagefilename)
        pygame.transform.scale(theimage, (thehwnd.get_width(),WINDOWHEIGHT) )
        thehwnd.blit( theimage, (0, BANNERHEIGHT) )
        display.flip()
    #endtry
        
    except Exception, e:
        print("display_background(): error '%s'" % str(e))
    #endexcept        

#enddef

#
#
# the purpose of this function is to check for a new player, an avatar with status of 'PLAYING'
def check_for_player(thehwnd, theconfigparser):

    print "check_for_player(): thehwnd=%s" % thehwnd
    print "check_for_player(): theconfigparser=%s" % theconfigparser

    try:

        # read the db configuration elements from the filename
        hostname=theconfigparser.get('databaseconnection', 'hostname')
        username=theconfigparser.get('databaseconnection', 'username')
        password=theconfigparser.get('databaseconnection', 'password')
        dbname=theconfigparser.get('databaseconnection', 'dbname')
        avatartablename=theconfigparser.get('databaseconnection', 'avatartablename')

        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT rownum,name FROM %s.%s WHERE status = 'PLAYING' ORDER BY queueposition ASC LIMIT 1" % (dbname, avatartablename)
        print "check_for_player(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        player_found = False

        # grab the important details from the record (should only be one)
        for row in cur.fetchall():
            player_found = True
        #endfor

        return player_found
    
    #endtry        
    except Exception, e:
        print("check_for_player(): error '%s'" % str(e))
    #endexcept
#enddef

#
#
# the purpose of this function is to calculate the player score based on the 'target' and 'actual' data
def calculate_highscore(target, actual):

    print "calculate_highscore(): target=%s" % target
    print "calculate_highscore(): actual=%s" % actual
    print "calculate_highscore(): len(target)=%d; len(actual)=%d" % (len(target), len(actual))

    try:

        maxscore = 0
        thescore = 0

        # calculate the score by adding the differences between the target[i] and actual[i]
        # the score return is the maximum possible score mimus the total differences
        for i in range(len(target)):
            maxscore += target[i]
            thescore += abs(target[i] - actual[i])
        #endfor

        print "calculate_highscore(); maxscore=%d; thescore=%d" % (maxscore, thescore)

        thehighscore = (maxscore - thescore)

        # prevent minus scores being returned
        if thehighscore < 0:
            thehighscore = 0
        #end if

        return thehighscore
    #endtry        

    except Exception, e:
        print("calculate_highscore(): error '%s'" % str(e))
    #endexcept
    
#enddef
#
# the purpose of this function is the main game, the function starts by drawing the target rpm profile from the configuration file
# the function then displays banners to guide the user before then pulse couting and finally dumping the data to binary file and the console
def do_game(thehwnd, thegpio, theconfigparser, maxsamples, startgpiopin, timeinternalseconds):

    print "do_game(): thehwnd=%s" % thehwnd
    print "do_game(): thegpio=%s" % thegpio
    print "do_game(): theconfigparser=%s" % theconfigparser
    print "do_game(): maxsamples=%s" % maxsamples
    print "do_game(): startgpiopin=%s" % startgpiopin
    print "do_game(): timeinternalseconds=%f" % timeinternalseconds
    
    try:

        # read the db configuration elements from the filename
        hostname=theconfigparser.get('databaseconnection', 'hostname')
        username=theconfigparser.get('databaseconnection', 'username')
        password=theconfigparser.get('databaseconnection', 'password')
        dbname=theconfigparser.get('databaseconnection', 'dbname')
        avatartablename=theconfigparser.get('databaseconnection', 'avatartablename')
        highscoretablename=theconfigparser.get('databaseconnection', 'highscoretablename')

        fontforecolour = [0, 0, 0]
        thestr = theconfigparser.get('general', 'fontforecolour')
        fontforecolour = thestr.split(',')

        backforecolour = [0, 0, 0]
        thestr = theconfigparser.get('general', 'fontbackcolour')
        fontbackcolour = thestr.split(',')
        
        #create the connection to the database
        db = MySQLdb.connect(host=hostname, user=username, passwd=password, db=dbname)
        
        #create a cursor for the select
        cur = db.cursor()
        
        # create a new row in the database and commit
        sqlcommandstr = "SELECT rownum,name,avatar FROM %s.%s WHERE status = 'PLAYING' ORDER BY queueposition ASC LIMIT 1" % (dbname, avatartablename)
        print "do_game(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)

        # grab the important details from the record (should only be one)
        for row in cur.fetchall():
            rownum = str(row[0])
            playername = str(row[1])
            imagedata = row[2]
        #endfor

        # write out the avatar image to disc
        filename = "%s.png" % playername
        write_file(imagedata, filename)    

        print "do_game(): player acquired {rownum=%s; playername=%s, filename=%s}" % (rownum, playername, filename)
        
        # reset and revs to stop display errors
        global revcount
        revcount=0

        # size the samples array and init to zero
        theProfileData=[0 for i in range(maxsamples)]
        myPulseData=[0 for i in range(maxsamples)]

        # draw the target reading from data file
        maxvalue = 0
        for i in range(maxsamples):

            # read profile data from config file and compute the target score
            theProfileData[i] = theconfigparser.getint('profiledata', '%d' % i)

            if theProfileData[i] > maxvalue:
                maxvalue = theProfileData[i]
            #endif

            # draw the data on the screen
            left = i * (thehwnd.get_width() / maxsamples)
            width = thehwnd.get_width() / maxsamples
            height = theProfileData[i] * (WINDOWHEIGHT / SINGLEPULSEBARHEIGHT)
            top = thehwnd.get_height() - height
            pygame.draw.rect ( thehwnd, Color(255,0,0), Rect(left, top, width, height), 0)
            pygame.draw.rect ( thehwnd, Color(0,255,0) , Rect(left, BANNERHEIGHT, width, PROGRESSBARHEIGHT), 0) 
            display.flip()
                   
        #endfor

        # debug print
        print "do_game(): target profile drawn"
            
        # add one more to the maxvalue enable clipping adding a small amount to show over peddling
        maxvalue += 1

        # display the "press start when ready" banner and wait for GPIO
        display_item_then_wait(thehwnd, thegpio, playername, fontbackcolour, fontforecolour, DISPLAY_TXT, "press START when ready...", WAIT_GPIO, startgpiopin)
        
        # display five second countdown timer
        for x in range(5, -1, -1):
            display_item_then_wait(thehwnd, thegpio, playername, fontbackcolour, fontforecolour, DISPLAY_TXT, "start peddling in %d ..." % x, WAIT_DELAY, 1)
        #endfor

        # determine whether a fake oeddle is needed
        fakepeddling=theconfigparser.getboolean('profiledata', 'fakepeddling')

        print "do_game(): fakepeddling=%s" % fakepeddling
        print "do_game(): maxvalue=%d" % maxvalue

        # display the player name whilst the game runs
        display_player_name(thehwnd, playername, BANNERHEIGHT + PROGRESSBARHEIGHT + (PROGRESSBARHEIGHT/2), fontbackcolour, fontforecolour)
        print "do_game(): game started"

        # Main loop that waits for the the call back handler to count then saves to array and dumps to screen
        loopcount = 0
        revcount = 0
                
        while loopcount < maxsamples :

            # if fakefeddling is configured, match the actual profile with a random difference and wait of 1/4 seconds, otherwaise wait a second
            if fakepeddling == True: 
                revcount = theProfileData[loopcount] + ( 2 - random.randint(0, 4) )
                time.sleep(0.1)
            else:
                time.sleep(timeinternalseconds)
            #endif
                
            # clip the revcount if it exceeds what can be drawn on the screen
            if revcount <= maxvalue:
                myPulseData[loopcount]=revcount
            else:
                print "do_game(): revcount clipped to %d" % maxvalue
                myPulseData[loopcount]=maxvalue
            #endif

            # reset the revcount in preparation for next cycle
            revcount = 0

            # draw the data on the screen
            left = loopcount * (thehwnd.get_width() / maxsamples)
            width = thehwnd.get_width() / maxsamples
            height = myPulseData[loopcount] * (WINDOWHEIGHT / SINGLEPULSEBARHEIGHT)
            top = thehwnd.get_height() - height
            pygame.draw.rect ( thehwnd, Color(0,255,0), Rect(left, top, width, height), 0)
            pygame.draw.rect ( thehwnd, Color(128,128,128) , Rect(left, BANNERHEIGHT, width, PROGRESSBARHEIGHT), 0) 
            display.flip()

            # debug print
            print "do_game(): loopcount=%d; maxsamples=%d; myPulseData[%d]=%d" % (loopcount, maxsamples, loopcount, myPulseData[loopcount])

            # reset counters and move to next sample        
            loopcount += 1        
            
        #endwhile

        print "do_game(): game finished, calculating score"

        # calculate the high score
        thehighscore = calculate_highscore(theProfileData, myPulseData)

        # update the score and the status
        sqlcommandstr = "UPDATE %s.%s SET gamehighscore='%d',status='COMPLETE',completiontime='%d' WHERE rownum='%s'" % (dbname, avatartablename, thehighscore, time.time(), rownum)
        print "do_game(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)
        db.commit()

        # dump the game date and high score
        sqlcommandstr ="INSERT INTO %s.%s (name,actualprofiledata,targetprofiledata,gamehighscore,completiontime) VALUES ('%s','%s','%s', %d, %d)" % (dbname, highscoretablename, playername, myPulseData, theProfileData, thehighscore, time.time())
        print "do_game(): sqlcommandstr=%s" % sqlcommandstr
        cur.execute(sqlcommandstr)
        db.commit()

        # announce complete, show the score and wait ten seconds
        display_item_then_wait(thehwnd, thegpio, playername, fontbackcolour, fontforecolour, DISPLAY_TXT, "finished! your score is %d" % thehighscore, WAIT_DELAY, 10)

        # delete the avatar image
        os.remove(filename)

        # close the cursor
        cur.close()

        # close the connection
        db.close()
    #endtry        
    except Exception, e:
        print("do_game(): error '%s'" % str(e))
    #endexcept
        
#endef    

#
# the purpose of this function is to act as the callback handler to count the pulses as the GPIO pin transitions low -> high
# the function is as bare as possible to preserve CPU cycles when called to minimize the changes of pulses being missed
def increaserev(channel):
    global revcount
    revcount += 1    
#enddef

#
#
# the purpose of this function is to display an amusing screen saver when the game is idling
def do_screensaver(thehwndwin):
    pass
#enddef

#
#
# the purpose of this function is the entry point for the software, it loads config varialbles, starts pygame and GPIO before invoking the main loop
def main(configfilename):

    try:

        print "main(): configfilename=%s" % configfilename

        # read the config file into the object
        config.read(configfilename)

        # read the application variables
        startbuttongpiopin = config.getint('general', 'startbuttongpiopin')
        pulsegpiopin = config.getint('general', 'pulsegpiopin')
        windowcaption = config.get('general', 'windowcaption')
        maxsamples = config.getint('general', 'maxsamples')
        timeinternalseconds = config.getfloat('general', 'timeinternalseconds')
        columnwidth = config.getint('general', 'columnwidth')
        backgroundimagefilename = config.get('general', 'backgroundimagefilename')
        bannerimagefilename = config.get('general', 'bannerimagefilename')
        fontname = config.get('general', 'fontname')
        fontsize = config.getint('general', 'fontsize')

        # debug print
        print ("main(): startbuttongpiopin=%d" % startbuttongpiopin)
        print ("main(): pulsegpiopin=%d" % pulsegpiopin)
        print ("main(): windowcaption=%s" % windowcaption)
        print ("main(): maxsamples=%d" % maxsamples)
        print ("main(): timeinternalseconds=%f" % timeinternalseconds)
        print ("main(): columnwidth=%d" % columnwidth)
        print ("main(): backgroundimagefilename=%s" % backgroundimagefilename)
        print ("main(): bannerimagefilename=%s" % bannerimagefilename)
        print ("main(): fontname=%s" % fontname)
        print ("main(): fontsize=%s" % fontsize)
        
        # setup the GPIO and variables and init array to zero
        g.setmode(g.BCM)
        g.setup(int(pulsegpiopin), g.IN)
        g.setup(int(startbuttongpiopin), g.IN)
        g.add_event_detect(int(pulsegpiopin), g.RISING, callback=increaserev)
        
        # init pygame, set the size and caption

        pygame.init()
        win = display.set_mode((maxsamples * columnwidth, WINDOWHEIGHT + BANNERHEIGHT))
        display.set_caption("Raspberry Pi Profiling game: " + windowcaption)

        # Set the font sizes
        global Font
        Font = font.SysFont(fontname, fontsize, bold=True, italic=False)
        
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
                        going = False
                    #endif                    
                #endif
            #endfor

            # check to see if a player is selected for play
            if check_for_player(win, config) == True:
                win.fill(Color(0, 0, 0), (0, BANNERHEIGHT, win.get_width(), win.get_height()))
                do_game(win, g, config, maxsamples, startbuttongpiopin, timeinternalseconds)
                display_background(win, bannerimagefilename, backgroundimagefilename)
            else:
                pass
            #endif

            # loop delay to preserve CPU
            time.sleep(0.5)

            # do a screen saver for ammusement
            do_screensaver(win)
            
        #endwhile

        # tidy yp pygame and GPIO and release
        pygame.quit()
        g.cleanup()
        return
    #endtry        
    except Exception, e:
        print("main(): error %s" % str(e))
    #endexcept
    
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
        