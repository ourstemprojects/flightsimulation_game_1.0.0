'''------------------------------------------------------------------------------------------------
Program:    app
Package:    1.4.0
Py Ver:     2.7
Purpose:    This program runs the scoreboard web interface for the digital engine simulator.

Dependents: json
            os
            pandas
            sys
            time
            base64
            flask
            db
            _version

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        To start the web interface:
            > python app.py

            In a browser, go to 127.0.0.1:5001
            [the host and port number are defined in config.json]

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
01.08.17    J. Berendt      0.0.1       Written
00.08.17    J. Berendt      0.0.?       Development updates.
04.08.17    J. Berendt      1.0.0       Initial stable release.
                                        Added -v and --version arguments for CLI version display.
                                        Removed unneeded / unused files from program structure.
                                        Wrapped getdata_* functions in try/except blocks.
                                        Moved player_delete, player_move, and player_playing
                                        methods to the db.DBConn class.  pylint(10/10)
09.08.17    J. Berendt      1.0.1       Enabled scoreboard refresh, at 2 seconds.
                                        Updated styles.css font-family element to add back-up
                                        fonts.
11.08.17    J. Berendt      1.1.0       Removed unneeded profile graph files.
                                        Removed unneeded background images.
                                        Updated right player panel to remove RESULTS FOR: title,
                                        as this text is now part of the profile graph.
                                        Updated minor css configuration around the change
                                        mentioned above.
11.08.17    J. Berendt      1.2.0       Added default profile graph to the
                                        Removed all player graphs from player_images directory.
14.08.17    J. Berendt      1.3.0       Added a gamedata db table creation call to the setup_db()
                                        function.  pylint (10/10)
22.08.17    J. Berendt      1.4.0       Generalised company branding for github.
                                        Added host, debug and threaded keys/values to config.json.
------------------------------------------------------------------------------------------------'''

import json
import os
import sys

from base64 import b64encode

import db
import pandas as pd

from flask import Flask, render_template, request, redirect
from _version import __version__


#SETUP GLOBAL APP OBJECT
APP = Flask(__name__)
APP.secret_key = 'devkey'

#ALLOW OPENING DOCSTRING
#pylint: disable=pointless-string-statement


#-----------------------------------------------------------------------
#FUNCTION READS AND RETURNS CONFIG FILE
def setup_config():

    return json.loads(open('config.json').read())


#-----------------------------------------------------------------------
#CREATE DBC INSTANCE (USED FOR DATABASE ACTIONS)
def setup_db():

    '''
    PURPOSE:
    Using the db.DBConn() class, this method is used to create the
    gamedata database table, if the table does not already exist, then
    return the connection object to the main() method.
    '''

    #CREATE DB INSTANCE
    dbc = db.DBConn(db_config_file='db_config.json')
    #ENSURE TABLE(S) IS/ARE CREATES
    dbc.create()

    #RETURN CONNECTION OBJECT
    return dbc


#-----------------------------------------------------------------------
#FUNCTION TO GET QUEUE DATA
def getdata_queue():

    '''
    PURPOSE:
    Function designed to get and return a dataframe populated with
    queue data, using the queue data SQL script.

    If an error occurs, an empty dataframe is returned.
    '''

    try:
        #CONNECT TO DB
        conn = DBC.connect()

        #READ QUERY
        qry = open(CFG['qry_getdata_queue']).read()
        #GET DATA
        data = pd.read_sql(qry, conn)

        #CLOSE DB CONNECTION
        conn.close()

        return data

    except Exception as err:
        #NOTIFICATION
        print 'ERR: Could not get queue data.'
        print 'ERR: %s' % err

        #RETURN AN EMPTY DATAFRAME
        return pd.DataFrame()


#-----------------------------------------------------------------------
#FUNCTION TO GET SCOREBOARD DATA
def getdata_scoreboard():

    '''
    PURPOSE:
    Function designed to get and return a dataframe populated with
    scoreboard data, using the scoreboard data SQL script.

    If an error occurs, an empty dataframe is returned.
    '''

    try:
        #CONNECT TO DB
        conn = DBC.connect()

        #READ QUERY
        qry = open(CFG['qry_getdata_scoreboard']).read()
        #GET DATA
        data = pd.read_sql(qry, conn)

        #CLOSE CONNECTION
        conn.close()

        return data

    except Exception as err:
        #NOTIFICATION
        print 'ERR: Could not get scoreboard data.'
        print 'ERR: %s' % err

        #RETURN AN EMPTY DATAFRAME
        return pd.DataFrame()


#-----------------------------------------------------------------------
#FUNCTION TO GET THE NAME AND AVATAR OF THE PLAYER CURRENTLY PLAYING
def getdata_now_playing():

    '''
    PURPOSE:
    Function designed to get and return a dataframe populated with
    the name and alias of the player who is currently playing, using
    the now_playing SQL script.

    If an error occurs, an empty dataframe is returned.

    DESIGN:
    The query returns the name and alias of the record with a 'status'
    of 'PLAYING'.

    If no players have a status of 'PLAYING', the dataframe is populated
    with default values, for display on the screen.
    '''

    try:
        #OPEN DB CONNECTION
        conn = DBC.connect()

        #READ QUERY
        qry = open(CFG['qry_getdata_now_playing']).read()
        #GET THE NAME OF WHO IS CURRENTLY PLAYING
        df_playing = pd.read_sql(qry, conn)

        #TEST IF DATA WAS FOUND
        if df_playing.empty:
            #IF NO DATA FOUND ADD DEFAULT VALUE TO FIELDS
            df_playing.loc[0, 'name'] = 'Who is next?'
            df_playing.loc[0, 'avatar'] = ''

        #CLOSE DB CONNECTION
        conn.close()

        #RETURN FRAME
        return df_playing

    except Exception as err:
        #NOTIFICATION
        print 'ERR: Could not get the name and avatar for the current player.'
        print 'ERR: %s' % err

        #RETURN AN EMPTY DATAFRAME
        return pd.DataFrame()


#-----------------------------------------------------------------------
#CENTERAL FUNCTION FOR GATHERING DATA FOR THE SCOREBOARD, AS A WHOLE
def compile_data():

    '''
    PURPOSE:
    The compile_data() function is used to compile all data used for the
    scoreboard, as a whole.  This allows flask's render_template()
    function for the scoreboard to be contained in a stand-alone
    function (pop_scoreboard()), to be called by other methods.

    DESIGN:
    The name and alias of the current player, the queue data and
    scoreboard data are compiled together, along with column names, are
    compiled into a dictionary and returned to the calling procedure.

    All data groups call the b64encode() function to transform the
    avatar's binary data (as collected form the database) into a
    displayable image.

    The column names are extracted into a list for each datagroup, for
    upper case conversion, and to enable the jinja template to iterate
    over the list, and populate the column names as required.

    The RANK column of the scoreboard is hard coded to a list of 1-5.
    '''

    try:
        #ALLOW LAMBDA FOR BINARY TO IMG CONVERSION
        #pylint: disable=unnecessary-lambda

        #GET NOW PLAYING DATA
        df_playing = getdata_now_playing()
        #CONVERT AVATAR DATA TO BASE64 STRING
        df_playing['avatar'] = df_playing['avatar'].apply(lambda img: b64encode(img))
        data_playing = df_playing.to_dict('records')[0]

        #GET DATA (QUEUE)
        df_queue = getdata_queue()
        #CONVERT AVATAR DATA TO BASE64 STRING
        df_queue['avatar'] = df_queue['avatar'].apply(lambda img: b64encode(img))
        #EXTRACT COLUMN NAMES FROM FRAME >> TO UPPER CASE
        cols_queue = [col.upper() for col in df_queue.columns]
        #CONVERT FRAME TO DICTIONARY FOR HTML TEMPLATE
        data_queue = df_queue.to_dict('records')

        #INITIALISE RANK NUMBER
        #GET DATA (SCOREBOARD)
        df_score = getdata_scoreboard()
        #CONVERT AVATAR DATA TO BASE64 STRING
        df_score['avatar'] = df_score['avatar'].apply(lambda img: b64encode(img))
        #ADD RANK FIELD FOR SCOREBOARD
        #(DYNAMIC RANK LIST (1-5) TO ALLOW FOR HIGH SCORES COUNTS < 5)
        df_score['rank'] = [idx for idx, _ in enumerate(df_score.index, 1)]
        #EXTRACT COLUMN NAMES FROM FRAME >> TO UPPER CASE
        cols_score = [col.upper() for col in df_score.columns]
        #CONVERT FRAME TO DICTIONARY FOR HTML TEMPLATE
        data_score = df_score.to_dict('records')

        #RETURN DICTIONARY OF DATASETS
        return dict(data_playing=data_playing,
                    data_queue=data_queue,
                    data_score=data_score,
                    columns_queue=cols_queue,
                    columns_score=cols_score)


    except Exception as err:
        #NOTIFICATION
        print 'ERR: Could not compile the data for the scoreboard.'
        print 'ERR: %s' % err

        #RETURN AN EMPTY DICTIONARY
        return dict()


#-----------------------------------------------------------------------
#POPULATE SCOREBOARD >> LOAD HOME PAGE (SCOREBOARD)
@APP.route('/')
def pop_scoreboard():

    '''
    PURPOSE:
    The sole purpose of this function is to populate the scoreboard.

    DESIGN:
    Flask's render_template() is called with the scoreboard.html
    template file and a *dictionary of data to be populated*.

    The dictionary argument has been shortcutted take advantage of
    Python's **kwargs capability.
    '''

    #LOAD PAGE AND PASS TEMPLATE DATA
    return render_template('scoreboard.html', **compile_data())


#-----------------------------------------------------------------------
#FUNCTION TO REMOVE A PLAYER FROM THE QUEUE
@APP.route('/player_delete')
def player_delete():

    '''
    PURPOSE:
    This function removes a player from the queue.

    DESIGN:
    Refer to the docstring (design section) for:
        - db.DBConn.player_delete()
    '''

    #UPDATE RECORD STATUS TO 'DELETED'
    DBC.player_delete(alias=request.args.get('alias'))

    #RELOAD SCOREBOARD
    return redirect('/')


#-----------------------------------------------------------------------
#FUNCTION USED TO MOVE A PLAYER TO THE BACK OF THE QUEUE
@APP.route('/player_move')
def player_move():

    '''
    PURPOSE:
    This function moves a player to the back of the queue.

    DESIGN:
    Refer to the docstring (design section) for:
        - db.DBConn.player_move()
    '''

    #MOVE A PLAYER TO THE BACK OF THE QUEUE
    DBC.player_move(alias=request.args.get('alias'))

    #RELOAD SCOREBOARD
    return redirect('/')


#-----------------------------------------------------------------------
#FUNCTION USED TO CHANGE A PLAYER'S STATUS 'PLAYING'
@APP.route('/player_playing')
def player_playing():

    '''
    PURPOSE:
    This function sets a player's status to 'PLAYING'.

    DESIGN:
    Refer to the docstring (design section) for:
        - db.DBConn.player_playing()
    '''

    #UPDATE A PLAYER'S STATUS TO 'PLAYING'
    DBC.player_playing(alias=request.args.get('alias'))

    #RELOAD SCOREBOARD
    return redirect('/')


#-----------------------------------------------------------------------
#MAIN CONTROLLER
def main():

    '''
    PURPOSE:
    This is the main program controller.

    DESIGN:
    The scoreboard's port is pulled from the config file.  Using a
    different port from the registration program allows the programs
    to be run in parallel, even from the same PC.
    '''

    #ALLOW GLOBALS
    #pylint: disable=global-variable-undefined

    global DBC
    global CFG

    DBC = setup_db()
    CFG = setup_config()

    #RUN APP
    APP.run(host=CFG['host'], port=CFG['port'],
            debug=CFG['app_debug'],
            threaded=CFG['app_threaded'])


#-----------------------------------------------------------------------
#RUN PROGRAM
if __name__ == '__main__':

    '''
    DESIGN:
    When run, the program searches for a '-v' or '--version' argument.
    If found, the script name and version (as defined in _version.py)
    are displayed to the CLI.

    If no arguments are found, the program is run.
    '''

    #TEST FOR ARGUMENTS
    if len(sys.argv) == 2:
        if sys.argv[1] == '-v' or sys.argv[1] == '--version':
            #GET PROGRAM NAME
            NAME = os.path.splitext(sys.argv[0])
            #PRINT VERSION NUMBER
            print '{prog} - v{version}'.format(prog=NAME[0], version=__version__)
    else:
        #RUN PROGRAM
        main()
