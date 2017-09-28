'''------------------------------------------------------------------------------------------------
Program:    calc
Version:    0.0.2
Platform:   Windows / Linux
Py Ver:     2.7
Purpose:    Game score calculator for the digital engine simulator game.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > from calc import calculate_highscore
            > score = calculate_highscore(target=target, actual=actual,
                                          return_zero=True)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
11.09.17    J. Berendt      0.0.1       Written
13.09.17    J. Berendt      0.0.2       Updated to return a score of 0.0, if the score to be
                                        returned is negative.
------------------------------------------------------------------------------------------------'''

import json
import pandas as pd
import numpy as np


#-----------------------------------------------------------------------
#FUNCTION TO READ THE CONFIG FILE
def _setup_config():

    return json.loads(open('config.json').read())


#-----------------------------------------------------------------------
#SCORE CALCULATION FUNCTION
def calculate_highscore(target, actual, return_zero=True):

    '''
    PURPOSE:
    This function is used to calculate the player's score for the
    digital engine simulator game.

    DESIGN:
    The function accepts two parameters, target and actual.  These
    parameters are both expected to be a python list of integers.

    Both lists are loaded into a pandas dataframe, where the absolute
    delta is calculated by wrapping the difference in the player's
    actual value and the target value in the numpy.abs() function.

    Next, each absolute delta is multiplied by a weight.  The weight is
    used to apply a greater penalty to the player's actual values
    farthest from the target value, and less for the player's actual
    values close to the target value.

    The sum of the weighted deltas is subtracted from the sum of the
    target values, and divided by the sum of the target values - in
    order to 'compress' the score to a value between 0 and 1 - then
    multiplied by 100 to create a 'human logical' score between 0 and
    100.

    This score is then returned to the bike program as a float, rounded
    to the number of decimal places as defined in the config file.

    If the return_zero flag is True, and the score to be returned is a
    negative value, a score of 0.0 is returned.

    PARAMETERS:
    - target
    A python list of integers containing the target profile array
    - actual
    A python list of integers containing the player's actual data
    array
    - return_zero (default=True)
    If the score to be returned is a negative value, return zero instead

    USE:
    from calc import calculate_highscore
    score = calculate_highscore(target=target, actual=actual,
                                return_zero=True)
    '''

    #GET VALUES FROM CONFIG
    cfg = _setup_config()

    #PULL TARGET AND ACTUAL PROFILES INTO FRAME
    df = pd.DataFrame({'TARGET':target, 'ACTUAL': actual})

    #CALC: DELTA
    df['DELTA'] = np.abs(df['ACTUAL'] - df['TARGET'])
    #CALC: WEIGHTED DELTA
    df['WEIGHTED'] = df['DELTA'] * cfg['weight']

    #CALCULATE SCORE
    score = ((df['TARGET'].sum() - df['WEIGHTED'].sum()) / df['TARGET'].sum()) * 100

    #SET SCORE TO ZERO IF RETURN_ZERO FLAG IS TRUE AND SCORE IS NEGATIVE
    score = 0.0 if return_zero is True and score < 0 else score

    #RETURN SCORE FORMATTED TO NUMBER OF DECIMAL PLACES SET IN CONFIG
    return round(score, cfg['score_decimal'])
