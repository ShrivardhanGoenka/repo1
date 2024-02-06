import psycopg2

def get_uid(token):
    try:
        # establish a connection
        connection = psycopg2.connect(
            dbname='techfest',
            user='avnadmin',
            password='AVNS_E8X_ovFZagLQJwM3eVH',
            host='pg-4147d0a-shrivardhangoenka-596a.aivencloud.com',
            port='14565',
            sslmode='require'
        )

        # create a cursor
        cursor = connection.cursor()

        # write your query
        query = "SELECT * FROM current_sign_in WHERE token = %s;"
        
        # execute the query
        cursor.execute(query, (token,))

        # fetch all the matching records
        records = cursor.fetchall()

        # close the cursor and the connection
        cursor.close()
        connection.close()

        # check if any record exists
        if records:
            return records[0][0]  # assuming uid column is the first one
        else:
            return False
            
    except (Exception, psycopg2.DatabaseError) as error:
        return False
    
def insert_audio(uid, key, name, genre, private, duration):
    try:
        connection = psycopg2.connect(
            dbname='techfest',
            user='avnadmin',
            password='AVNS_E8X_ovFZagLQJwM3eVH',
            host='pg-4147d0a-shrivardhangoenka-596a.aivencloud.com',
            port='14565',
            sslmode='require'
        )

        # create a cursor
        cursor = connection.cursor()

        # write your query
        query = "INSERT INTO audio (uid, key, name, genre, private, duration) VALUES (%s, %s, %s, %s, %s, %s);"

        # execute the query
        cursor.execute(query, (uid, key, name, genre, private, duration))

        # commit the changes
        connection.commit()

        # close the cursor and the connection
        cursor.close()
        connection.close()

        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return False
            