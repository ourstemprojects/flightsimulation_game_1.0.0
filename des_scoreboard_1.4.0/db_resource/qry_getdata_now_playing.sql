
-- GET PLAYER NOW PLAYING
SELECT
      name
    , avatar
FROM
    avatardata
WHERE
    UPPER(status) = 'PLAYING'