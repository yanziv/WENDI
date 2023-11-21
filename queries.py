import cs304dbi as dbi


def show_rooms(conn, dormid):
    '''return all rooms with specified dormid as the hid'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select number from room2 where hid = %s
    ''', [dormid])
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