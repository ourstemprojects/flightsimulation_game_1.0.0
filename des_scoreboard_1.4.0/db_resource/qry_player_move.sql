
-- MOVE A PLAYER TO THE BACK OF THE QUEUE
UPDATE
    avatardata
SET
    queueposition = %s 
WHERE
    name = %s