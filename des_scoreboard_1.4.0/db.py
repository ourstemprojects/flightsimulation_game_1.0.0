'''------------------------------------------------------------------------------------------------
Program:    db.py
Version:    0.2.1
Py Ver:     2.7
Purpose:    Database class for the pibike scoreboard interface.

Dependents: json
            mysql.connector
            pandas
            time

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        >
            >

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
02.08.17    J. Berendt      0.1.0       Copied from rrfd_avatar module.
                                        Commented the following methods:
                                            - create(), insert(), user_exists(), _close()
07.08.17    J. Berendt      0.1.1       Added docstrings to each applicable method / function.
                                        Added try/except block to connect().
                                        Updated player_delete query to change status to 'DELETED'
                                        rather than removing the record from the database.
                                        Updated queue query to pull records where the status does
                                        not equal 'COMPLETE' or 'DELETED'.
                                        Moved player_move, player_delete and now_playing methods
                                        from app.py, to this module.  pylint(10/10)
14.08.17    J. Berendt      0.2.0       Added a create() method to create the db table on class
                                        instantiation, if it doesn't already exist.
24.08.17    J. Berendt      0.2.1       Generalised company branding for github.
------------------------------------------------------------------------------------------------'''

import json
import time
import pandas as pd
import mysql.connector


class DBConn(object):

    #-------------------------------------------------------------------
    #INITIALISATION
    def __init__(self, db_config_file):

        #READ IN CONFIG FILES
        self._db_config = json.loads(open(db_config_file).read())
        self._config    = json.loads(open('config.json').read())


    #-------------------------------------------------------------------
    #FUNCTION RETURNS THE DB CONNECTION OBJECT
    def connect(self):

        '''
        DESIGN:
        A dictionary containing the database login credentials are kept
        in the db_config.json file, which is read into the
        self._db_config variable on class instantiation.

        This dictionary is passed into the mysql.connector.connect()
        function as a **kwargs argument.
        '''

        try:
            #RETURN A CONNECTION TO THE DATABASE
            return mysql.connector.connect(**self._db_config)

        except Exception as err:
            #NOTIFICATION
            print 'ERR: Could not connect to the database.'
            print 'ERR: %s' % err


    #-------------------------------------------------------------------
    #ENSURE DB TABLE(S) IS/ARE CREATED
    def create(self):

        '''
        PURPOSE:
        This method is used to create the gamedata table.

        DESIGN:
        This method should be called *once* on program startup; perhaps
        from the main() method of the program.

        The create script is contained in the
        /db_resource/qry_create_gamedata.sql file.
        '''

        try:
            #CREATE CONNECTION AND CURSOR OBJECTS
            conn = self.connect()
            cur  = conn.cursor()

            #READ QUERY
            qry = open(self._config['qry_create_gamedata']).read()

            #EXECUTE / COMMIT / CLOSE CONNECTION
            cur.execute(qry)
            conn.commit()
            conn.close()

        except Exception as err:
            #NOTIFICATION
            print 'ERR: An error occurred while creating the table.'
            print 'ERR: %s' % err


    #-------------------------------------------------------------------
    #METHOD USED TO DELETE A PLAYER FROM THE QUEUE
    def player_delete(self, alias):

        '''
        PURPOSE:
        The player_delete() method is used to remove a player from the
        queue.

        DESIGN:
        The player's record *is not* deleted, however their 'status'
        is changed to 'DELETED'.
        '''

        try:
            #CONNECT TO DB >> GEGT CURSOR OBJECT
            conn = self.connect()
            cur = conn.cursor()

            #READ AND EXECUTE QUERY
            qry = open(self._config['qry_player_delete']).read()
            cur.execute(qry, (alias,))

            #COMMIT AND CLOSE CONNECTION
            conn.commit()
            conn.close()

        except Exception as err:
            #NOTIFICATION
            print 'ERR: An error occurred while deleting player: (%s)' % alias
            print 'ERR: %s' % err


    #-------------------------------------------------------------------
    #METHOD USED TO MOVE A PLAYER TO THE BACK OF THE QUEUE
    def player_move(self, alias):

        '''
        PURPOSE:
        The player_move() method is used to move a player to the back
        of the queue.

        DESIGN:
        The player's queueposition value is updated to the current
        epoch time; thus pushing the player to the back of the order.
        '''

        try:
            #GET CURRENT EPOCH TIME (USED AS THE NEW QUEUEPOSITION VALUE)
            epoch = int(time.time())

            #CONNECT TO DB >> GET CURSOR OBJECT
            conn = self.connect()
            cur = conn.cursor()

            #READ AND EXECUTE QUERY
            qry = open(self._config['qry_player_move']).read()
            cur.execute(qry, (epoch, alias))

            #COMMIT AND CLOSE CONNECTION
            conn.commit()
            conn.close()

        except Exception as err:
            #NOTIFICATION
            print 'ERR: An error occurred while moving player (%s) to the back of the '\
                  'queue.' % alias
            print 'ERR: %s' % err


    #-------------------------------------------------------------------
    #METHOD TO SET A PLAYER'S STATUS TO PLAYING
    def player_playing(self, alias):

        '''
        PURPOSE:
        The player_playing() method is used to set a player's status
        to 'PLAYING'.

        DESIGN:
        The player's status is updated to 'PLAYING' after first
        verifying another player does not already have a 'PLAYING'
        status.

        If other players are found with a 'PLAYING' status, a
        STATUS ERROR is output to the console showing a list of player
        names with a 'PLAYING' status.
        '''

        try:
            #CONNECT TO DB >> GET CURSOR OBJECT
            conn = self.connect()
            cur = conn.cursor()

            #GET COUNT OF RECORDS WITH STATUS OF 'PLAYING'
            qry_playing = open(self._config['qry_count_playing']).read()
            cur.execute(qry_playing)
            count = cur.fetchall()[0][0]

            #TEST IF ANOTHER PLAYER IS PLAYING
            if count == 0:
                #UPDATE PLAYER STATUS TO 'PLAYING'
                qry = open(self._config['qry_player_playing']).read()
                cur.execute(qry, (alias, ))
                conn.commit()
            else:
                #GET NAME OF PLAYER ALREADY PLAYING
                df = pd.read_sql(sql=open(self._config['qry_getdata_now_playing']).read(),
                                 con=conn)
                #PRINT TROUBLESHOOTING ERROR TO CONSOLE
                print "STATUS ERROR: These players already have a status of 'PLAYING': %s" \
                      % df['name'].tolist()

            #CLOSE DB CONNECTION
            conn.close()

        except Exception as err:
            #NOTIFICATION
            print "ERR: An error occurred while updating player (%s) to 'PLAYING'" % alias
            print 'ERR: %s' % err
