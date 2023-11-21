import cs304dbi as dbi


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