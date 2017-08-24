
-- GET DATA FOR QUEUE
SELECT
      status
    , name
    , avatar
FROM
    avatardata
WHERE
    UPPER(status) not in ('COMPLETE', 'DELETED')
ORDER BY
    queueposition ASC 
LIMIT 5