import cs304dbi as dbi


def show_rooms(conn, hall_id):
    """return all rooms with specified hall_id as the hid"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select number from room where hid = %s
    """,
        [hall_id],
    )
    return curs.fetchall()


def show_reviews(conn, roomid):
    """return all reviews made for specified room"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select * from review where rid = %s
    """,
        [roomid],
    )
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


def search_by_hid_or_number(conn, search_term):
    query = "SELECT hid, number FROM room WHERE hid LIKE %s OR number LIKE %s"
    params = ("%" + search_term + "%", "%" + search_term + "%")

    cursor = conn.cursor()
    cursor.execute(query, params)

    results = cursor.fetchall()
    cursor.close()

    return results


def search_by_hid_and_number(conn, search_term):
    # Split the search term into individual terms
    terms = search_term.split()

    # Use individual terms to search for both hid and number
    if len(terms) >= 2:
        query = "SELECT hid, number FROM room WHERE hid LIKE %s AND number LIKE %s"
        params = ("%" + terms[0] + "%", "%" + terms[1] + "%")
    elif len(terms) == 1:
        # Handle the case where there's only one term
        query = "SELECT hid, number FROM room WHERE hid LIKE %s OR number LIKE %s"
        params = ("%" + terms[0] + "%", "%" + terms[0] + "%")
    else:
        # Handle the case where there are no terms
        return []

    cursor = conn.cursor()
    cursor.execute(query, params)

    results = cursor.fetchall()
    cursor.close()

    return results
