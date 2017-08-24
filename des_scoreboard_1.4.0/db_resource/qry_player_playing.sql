
-- UPDATE STATUS TO PLAYING
UPDATE
    avatardata
SET
    status = 'PLAYING' 
WHERE
    name = %s