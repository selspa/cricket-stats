import os
import psycopg
from psycopg.rows import dict_row
import time

def connect(retry_interval=5, max_retries=10):
    
    connection_params = {}
    conn = None
    for attempt in range(max_retries):
        try:
            # connect to the PostgreSQL server
            conn = psycopg.connect(
                user = os.getenv("DATABASE_USERNAME"),                                      
                password = os.getenv("DATABASE_PASSWORD"),                                  
                host = os.getenv("DATABASE_HOST"),                                            
                port = os.getenv("DATABASE_PORT"),                                          
                dbname = os.getenv("DATABASE_NAME") 
                )
        except:
            conn = "error"
            print(f"Attempt {attempt + 1} failed, retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

        if conn != "error":
            # create a cursor
            cur = conn.cursor(row_factory=dict_row)
        else: 
            cur = "error"
            
        connection_params = {"connection": conn, "cursor": cur}

    return connection_params
