
-- CREATE GAMEDATA TABLE
CREATE TABLE IF NOT EXISTS gamedata (
      rownum                INTEGER         PRIMARY KEY  AUTO_INCREMENT  UNIQUE  NOT NULL
    , name                  VARCHAR(32)     NOT NULL
    , actualprofiledata     BLOB            NOT NULL
    , targetprofiledata     BLOB            NOT NULL
    , gamehighscore         BIGINT          NOT NULL
    , completiontime        INT             DEFAULT NULL
    , profiled              BOOL            DEFAULT 0
    )
