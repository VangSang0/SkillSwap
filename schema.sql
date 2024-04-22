-- For now, creating tables into a dummydata database for testing purposes
-- This will be changed to a real database in the future

-- CREATE DATABASE IF NOT EXISTS dummydata; just in case we need to create the database


CREATE TABLE IF NOT EXISTS Users(
    user_id         SERIAL,   
    first_name      VARCHAR(225)    NOT NULL,   
    last_name       VARCHAR(225)    NOT NULL,   
    email           VARCHAR(225)    NOT NULL, 
    username        VARCHAR(225)    NOT NULL,  
    is_TA           BOOLEAN         NOT NULL,
    hash_pass       VARCHAR(225)    NOT NULL,   
    concentration   VARCHAR(255),

    PRIMARY KEY(user_id)
);


CREATE TABLE IF NOT EXISTS Posts(
    post_id         SERIAL,
    post_author_id  INTEGER         NOT NULL,
    num_likes       INTEGER,    
    num_comments    INTEGER,
    datetime_post   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    post_conent     VARCHAR(255)    NOT NULL,

    PRIMARY KEY (post_id),
    FOREIGN KEY (post_author_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Comments(
    comment_id          SERIAL,
    comment_author_id   INTEGER         NOT NULL,
    post_id             INTEGER         NOT NULL,
    datetime_posted     TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    content             VARCHAR(255)    NOT NULL,

    PRIMARY KEY(comment_id),
    FOREIGN KEY (comment_author_id)   REFERENCES Users(user_id),
    FOREIGN KEY (post_id)             REFERENCES Posts(post_id)

);

CREATE TABLE IF NOT EXISTS Courses(
    course_id       SERIAL,
    course_name     VARCHAR(225)    NOT NULL,
    credit_hrs      INTEGER         NOT NULL,


    PRIMARY KEY(course_id)
);

CREATE TABLE IF NOT EXISTS User_Friends(
    user_id              INTEGER    NOT NULL,
    friend_user_id       INTEGER    NOT NULL,


    PRIMARY KEY (user_id, friend_user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );

CREATE TABLE IF NOT EXISTS User_Courses(
    user_id         INTEGER    NOT NULL,
    course_id       INTEGER    NOT NULL,

    PRIMARY KEY(user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
