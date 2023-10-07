# import OS (allows to access env variables)
import os
# import psycopg2 (allows to connect to Postgres)
import psycopg2
# Import DictCursor (allows to access data by column name)
from psycopg2.extras import DictCursor

def run_query(sql, params=None):
     #  Get the database URL form the environment variables
    DATABASE_URL = os.environ.get('DATABASE_URL')

    # Make sure the databse URL exists
    if not DATABASE_URL:
        raise ValueError('DATABASE_URL is not set')

    # Establish the connection
    with psycopg2.connect(DATABASE_URL) as conn:
        # Create a curser Objects
        with conn.cursor(cursor_factory=DictCursor) as cur:
            # Execute the sql
            cur.execute(sql, params)
            # Check if command is a Select statement
            if cur.description:
                return cur.fetchall()
            else:
                None