
-- REMOVE A PLAYER FROM THE QUEUE
UPDATE
    avatardata 
SET
    status = 'DELETED' 
WHERE
    name = %s