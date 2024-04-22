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



def add_post(user_id: int, post_content: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO Posts (user_id, content)
                            VALUES (%s, %s)
                            RETURNING post_id
                            ''', [user_id, post_content])
            post_id = cursor.fetchone()
            if post_id is None:
                raise Exception('Post not created')
            else:
                return post_id