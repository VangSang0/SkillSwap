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
                                app_user 
                            WHERE 
                                username = %s
                            ''', [username])
            user_id = cursor.fetchone()
            return user_id is not None
        
def create_user(username: str, password: str):
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                            INSERT INTO app_user (username, password)
                            VALUES (%s, %s)
                            RETURNING user_id
                            ''', [username, password])
            user_id = cursor.fetchone()
            if user_id is None:
                raise Exception('User not created')
            else:
                return {'user_id': user_id,
                        'username': username}

def get_user_by_username(username: str) -> dict[str, Any] | None:  
    pool = get_pool()
    with pool.connection() as connection:
        with connection.cursor(cursor_factory=dict_row) as cursor:
            cursor.execute('''
                            SELECT 
                                user_id, 
                                username,
                                password AS hashed_password
                            FROM 
                                app_user 
                            WHERE 
                                username = %s
                            ''', [username])
            user = cursor.fetchone()
            if user is None:
                return None
            else:
                return user
            