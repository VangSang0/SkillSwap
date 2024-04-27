from typing import Any
from repositories.db import get_pool
from psycopg.rows import dict_row


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