import cs304dbi as dbi
from flask import flash

def insert_media(conn,url,uid,rid,cid):
    """
    Uploads media to the table for room reviews.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute("""insert into media(url,uid,rid,cid) 
                    values (%s,%s,%s,%s)""",
                    [url,uid,rid,cid])
    conn.commit()

def get_all_dorms(conn):
    """
    Returns info regarding all residential halls at Wellesley.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select * from hall"""
    )
    return curs.fetchall()

def get_rid_given_hall_and_number(conn,hall,number):
    """
    Returns room id (id in the room table) given the 3-letter
    hall encoding and specific room number.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select id from room
        where number = %s 
        and hid = %s''',
        [number,hall])
    return curs.fetchone()


def get_hid_given_hall_name(conn,hall_name):
    """
    Returns the three-letter encoding hid of a given residential hall.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select id from hall
        where name = %s""",
        [hall_name],
    )
    return curs.fetchone()


def insert_review(
    conn,
    uid,
    rid,
    rating,
    startTime,
    lengthOfStay,
    sizeScore,
    storageScore,
    ventScore,
    cleanScore,
    bathroomScore,
    accessibilityScore,
    sunlightScore,
    bugScore,
    windowScore,
    noiseScore,
    comment,
    hasMedia,
    timePosted,
):
    """
    Insert user review into the review table in wendi_db 
    and return the review_id.
    """
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """insert into review(uid,rid,rating,startTime,
                    lengthOfStay,sizeScore,storageScore,ventScore,
                    cleanScore,bathroomScore,accessibilityScore,
                    sunlightScore,bugScore,windowScore,noiseScore,
                    comment,hasMedia,timePosted)
                    values (%s, %s, %s, %s,%s, %s, %s, %s,
                    %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)""",
        [
            uid,
            rid,
            rating,
            startTime,
            lengthOfStay,
            sizeScore,
            storageScore,
            ventScore,
            cleanScore,
            bathroomScore,
            accessibilityScore,
            sunlightScore,
            bugScore,
            windowScore,
            noiseScore,
            comment,
            hasMedia,
            timePosted,
        ],
    )
    # Retrieve the last insert id
    curs.execute("select last_insert_id()")
    row = curs.fetchone()
    conn.commit()
    return row['last_insert_id()']


def show_rooms(conn, hall_id):
    """return all rooms with specified hall_id as the hid"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select number, type, description from room where hid = %s
    """,
        [hall_id],
    )
    return curs.fetchall()


def sort_rooms_by(conn, hall_id, criteria):
    """ "returns all rooms with specified hall_id by the criteria entered"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select number, type, description from room where hid = %s and description = %s
        """,
        [hall_id, criteria],
    )
    return curs.fetchall()


def get_room_types(conn, hall_id):
    """returns all room types in specified hall"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select distinct description from room where hid = %s
        """,
        [hall_id],
    )
    return curs.fetchall()


def show_reviews(conn, roomnum):
    """return all reviews made for specified room"""
    curs = dbi.dict_cursor(conn)
    curs.execute(
        """
        select room.number as rid, room.description as description, rating, startTime, lengthOfStay, cleanScore, bathroomScore, sizeScore, ventScore, accessibilityScore,
        sunlightScore, bugScore, windowScore, noiseScore, comment, timePosted from review, room where review.rid = room.id and room.number = %s
    """,
        [roomnum],
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
