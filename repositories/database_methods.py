from typing import Any
from repositories.db import get_pool
from psycopg.rows import dict_row
import psycopg
from typing import Tuple
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


def does_user_exist(username: str) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT 
                                user_id
                            FROM 
                                Users 
                            WHERE 
                                username = %s
                            ''', [username])
            user_id = cursor.fetchone()
            return user_id is not None

def does_email_exist(email: str) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT 
                                user_id
                            FROM 
                                Users 
                            WHERE 
                                email = %s
                            ''', [email])
            user_id = cursor.fetchone()
            return user_id is not None

def create_user(first_name : str, last_name : str, user_email: str, username: str, hashed_password: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO Users (first_name, last_name, email, username, hash_pass)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING user_id
                            ''', [first_name, last_name, user_email, username, hashed_password])
            user_id = cursor.fetchone()
            if user_id is None:
                raise Exception('User not created')
            else:
                return {'user_id': user_id,
                        'username': username}

def get_user_by_username(username: str) -> dict[str, Any] | None:  
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                user_id, 
                                username,
                                hash_pass AS hashed_password
                            FROM 
                                Users 
                            WHERE 
                                username = %s
                            ''', [username])
            user = cursor.fetchone()
            if user is None:
                return None
            else:
                return user

def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                user_id, 
                                username
                            FROM 
                                Users 
                            WHERE 
                                user_id = %s
                            ''', [user_id])
            user = cursor.fetchone()
            if user is None:
                return None
            else:
                return user



def add_post(post_author_id: int, post_content: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO Posts (post_author_id, post_content)
                            VALUES (%s, %s)
                            RETURNING post_id
                            ''', [post_author_id, post_content])
            post_id = cursor.fetchone()
            if post_id is None:
                raise Exception('Post not created')
            else:
                return post_id


def get_all_posts():
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                Posts.post_id,
                                Posts.post_author_id,
                                Users.username AS author,
                                Posts.num_likes,
                                Posts.num_comments,
                                Posts.datetime_post,
                                Posts.post_content
                            FROM 
                                Posts
                            JOIN
                                Users
                            ON
                                Posts.post_author_id = Users.user_id
                            ORDER BY 
                                datetime_post ASC
                            ''')
            posts = cursor.fetchall()
            return posts


def get_post_by_id(post_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                Posts.post_id, 
                                Posts.post_author_id,
                                Users.username AS author,
                                Posts.num_likes,
                                Posts.num_comments,
                                Posts.datetime_post,
                                Posts.post_content
                            FROM 
                                Posts
                            JOIN
                                Users
                            ON
                                Posts.post_author_id = Users.user_id
                            WHERE
                                post_id = %s
                            ''', [post_id])
            post = cursor.fetchone()
            return post

def get_posts_by_user_id(user_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                Posts.post_id, 
                                Posts.post_author_id,
                                Users.username AS author,
                                Posts.num_likes,
                                Posts.num_comments,
                                Posts.datetime_post,
                                Posts.post_content
                            FROM 
                                Posts
                            JOIN
                                Users
                            ON
                                Posts.post_author_id = Users.user_id
                            WHERE
                                post_author_id = %s
                            ORDER BY 
                                datetime_post ASC
                            ''', [user_id])
            posts = cursor.fetchall()
            return posts
        
def delete_post(post_id: int) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            DELETE FROM 
                                Posts
                            WHERE
                                post_id = %s
                            ''', [post_id])
            # what can I return here?


def edit_post(post_id: int, post_content: str) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            UPDATE 
                                Posts
                            SET
                                post_content = %s
                            WHERE
                                post_id = %s
                            ''', [post_content, post_id])
            # what can I return here?


def add_comment(comment_author_id: int, post_id: int, comment_content: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO Comments (comment_author_id, post_id, content)
                            VALUES (%s, %s, %s)
                            RETURNING comment_id
                            ''', [comment_author_id, post_id, comment_content])
            comment_id = cursor.fetchone()
            if comment_id is None:
                raise Exception('Comment not created')
            else:
                return comment_id
            
def get_comments_by_post_id(post_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                Comments.comment_id,
                                Comments.comment_author_id,
                                Users.username AS author,
                                Comments.datetime_posted,
                                Comments.content
                            FROM 
                                Comments
                            JOIN
                                Users
                            ON
                                Comments.comment_author_id = Users.user_id
                            WHERE
                                post_id = %s
                            ORDER BY 
                                datetime_posted ASC
                            ''', [post_id])
            comments = cursor.fetchall()
            return comments
          
def get_comment_by_id(comment_id: int):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                Comments.comment_id,
                                Comments.comment_author_id,
                                Users.username AS author,
                                Comments.datetime_posted,
                                Comments.content
                            FROM 
                                Comments
                            JOIN
                                Users
                            ON
                                Comments.comment_author_id = Users.user_id
                            WHERE
                                comment_id = %s
                            ''', [comment_id])
            comment = cursor.fetchone()
            return comment

def delete_comment(comment_id: int) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            DELETE FROM 
                                Comments
                            WHERE
                                comment_id = %s
                            ''', [comment_id])
            # what can I return here?

def edit_comment(comment_id: int, comment_content: str) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            UPDATE 
                                Comments
                            SET
                                content = %s
                            WHERE
                                comment_id = %s
                            ''', [comment_content, comment_id])
            # what can I return here?


def toggle_like(user_id: int, post_id: int) -> Tuple[int, str]:
    pool = get_pool()  # Assume get_pool returns a connection pool
    operation = 'unlike'  # Default operation

    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                # Check if the like already exists
                cursor.execute('''
                    SELECT like_id FROM Post_Likes
                    WHERE user_id = %s AND post_id = %s
                ''', (user_id, post_id))
                like = cursor.fetchone()
                
                if like:
                    # Like exists, so remove it
                    cursor.execute('''
                        DELETE FROM Post_Likes
                        WHERE like_id = %s
                    ''', (like[0],))
                    cursor.execute('''
                        UPDATE Posts
                        SET num_likes = num_likes - 1
                        WHERE post_id = %s
                        RETURNING num_likes
                    ''', (post_id,))
                    new_like_count = cursor.fetchone()[0]
                else:
                    # Like does not exist, so add it
                    cursor.execute('''
                        INSERT INTO Post_Likes (post_id, user_id)
                        VALUES (%s, %s)
                    ''', (post_id, user_id))
                    cursor.execute('''
                        UPDATE Posts
                        SET num_likes = num_likes + 1
                        WHERE post_id = %s
                        RETURNING num_likes
                    ''', (post_id,))
                    new_like_count = cursor.fetchone()[0]
                    operation = 'like'  # Update operation since a like was added
                
                # Commit the transaction
                connection.commit()

                # Prevent negative like count
                if new_like_count < 0:
                    cursor.execute('''
                        UPDATE Posts
                        SET num_likes = 0
                        WHERE post_id = %s
                    ''', (post_id,))
                    new_like_count = 0
                    connection.commit()

                return new_like_count, operation

    except psycopg.DatabaseError as e:
        # Proper error handling/log message should go here
        print("Database error:", e)
        # Optionally, re-raise the error after logging it
        raise


        
def get_like_count(post_id: int) -> int:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT num_likes FROM Posts 
                            WHERE post_id = %s
                            ''', [post_id])
            result = cursor.fetchone()
            return result[0] if result else 0
        
def check_user_like(user_id: int, post_id: int) -> bool:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            SELECT 1 FROM Post_Likes 
                            WHERE user_id = %s AND post_id = %s
                            ''', (user_id, post_id))
            return cursor.fetchone() is not None            

def get_user_information_by_id(user_id: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                first_name,
                                last_name,
                                email,
                                username,
                                concentration
                            FROM 
                                users
                            WHERE 
                                user_id = %s
                            ''', [user_id])
            user = cursor.fetchone()
            return user


def get_user_friends(user_id):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT U.user_id, U.username, COUNT(MF.friend_user_id) AS mutual_friends_count
                FROM Users U
                JOIN User_Friends UF ON U.user_id = UF.friend_user_id
                LEFT JOIN User_Friends MF ON U.user_id = MF.user_id AND MF.friend_user_id = UF.user_id
                WHERE UF.user_id = %s
                GROUP BY U.user_id
            ''', [user_id])
            friends = cursor.fetchall()
            return friends
        
def add_friend(user_id, friend_id):
    pool = get_pool()
    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO User_Friends (user_id, friend_user_id) VALUES (%s, %s)', (user_id, friend_id))
    except Exception as e:
        raise e


def check_friendship(user_id, friend_id):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1 FROM User_Friends WHERE user_id = %s AND friend_user_id = %s', (user_id, friend_id))
            return cursor.fetchone() is not None


def get_incoming_friend_requests(user_id):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT U.user_id, U.username, COUNT(MF.friend_user_id) AS mutual_connections
                FROM Users U
                JOIN User_Friends UF ON U.user_id = UF.user_id
                LEFT JOIN User_Friends MF ON U.user_id = MF.user_id AND MF.friend_user_id = UF.friend_user_id
                WHERE UF.friend_user_id = %s AND MF.friend_user_id IS NULL
                GROUP BY U.user_id
            ''', [user_id])
            requests = cursor.fetchall()
            return requests
        
def get_user_by_id(user_id: int) -> dict[str, Any] | None: #settings(nicole)
   pool = get_pool()
   with pool.connection() as connection:
       with connection.cursor(row_factory=dict_row) as cursor:
           cursor.execute('''
                           SELECT
                               user_id,
                               username,
                               first_name,
                               last_name,
                               email,
                               concentration,
                               hash_pass AS hashed_password
                           FROM
                               Users
                           WHERE
                               user_id = %s
                           ''', [user_id])
           user = cursor.fetchone()
           if user is None:
               return None
           else:
               return user


def update_user_settings(user_id: int, email: str, first_name: str, last_name: str):
   pool = get_pool()
   with pool.connection() as connection:
       with connection.cursor() as cursor:
           cursor.execute('''
                           UPDATE Users
                           SET email = %s, first_name = %s, last_name = %s
                           WHERE user_id = %s
                           ''', [email, first_name, last_name, user_id])
           connection.commit()


def update_username(user_id: int, new_username: str):
   pool = get_pool()
   with pool.connection() as connection:
       with connection.cursor() as cursor:
           cursor.execute('''
                           UPDATE Users
                           SET username = %s
                           WHERE user_id = %s
                           ''', [new_username, user_id])
           connection.commit()


def update_password(user_id: int, hashed_password: str):
   pool = get_pool()
   with pool.connection() as connection:
       with connection.cursor() as cursor:
           cursor.execute('''
                           UPDATE Users
                           SET hash_pass = %s
                           WHERE user_id = %s
                           ''', [hashed_password, user_id])
           connection.commit()


def update_concentration(user_id: int, concentration: str):
   pool = get_pool()
   with pool.connection() as connection:
       with connection.cursor() as cursor:
           cursor.execute('''
                           UPDATE Users
                           SET concentration = %s
                           WHERE user_id = %s
                           ''', [concentration, user_id])
           connection.commit()


def search_users(username: str) -> list[dict[str, Any]]:
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT user_id, username
                FROM Users
                WHERE username ILIKE %s
            ''', [f"%{username}%"])
            users = cursor.fetchall()
            return users