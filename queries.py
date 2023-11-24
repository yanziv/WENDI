import cs304dbi as dbi

def get_all_dorms(conn):
    """
    Returns info regarding all residential halls at Wellesley.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from hall''')
    return curs.fetchall()

def get_hid_given_hall_name(conn,hall_name):
    """
    Returns the three-letter encoding hid of a given residential hall.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select id from hall
        where name = %s''', [hall_name])
    return curs.fetchone()

def review(conn,tt,title,release,addedby):
    """
    After checking tt doesn't exist in the movie table in wmdb,
    proceed to insert this new movie into wmdb.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''insert into review(tt,title,release,addedby)
                    values (%s, %s, %s, %s)''',[tt,title,release,addedby])
    conn.commit()

def show_rooms(conn, hall_id):
    '''return all rooms with specified hall_id as the hid'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select number from room where hid = %s
    ''', [hall_id])
    return curs.fetchall()


def show_reviews(conn, roomid):
    '''return all reviews made for specified room'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from review where rid = %s
    ''', [roomid])
    return curs.fetchall()

def authenticate_user(username, password):
    """Check if the username and password match."""
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        SELECT * FROM user WHERE username = %s AND password = %s
        """,
        [username, password],
    )
    result = curs.fetchone()
    return result is not None  # It returns True if authentication successful.