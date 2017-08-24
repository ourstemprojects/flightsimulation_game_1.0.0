
-- GET DATA FOR SCOREBOARD
SELECT 
      gamehighscore
    , name
    , avatar
FROM
    avatardata
WHERE
    UPPER(status) = 'COMPLETE'
ORDER BY
    gamehighscore DESC 
LIMIT 5