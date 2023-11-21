import cs304dbi as dbi

def show_rooms(conn, hallid):
    '''return all rooms with specified dormid as the hid'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select number from room where hid = %s
    ''', [hallid])
    return curs.fetchall()

def show_reviews(conn, roomid):
    '''return all reviews made for specified room. each review consists of review id,
        rid, rating, comment, score for all criteria, user information, image
        '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select review.id, rid, rating, comment from review where rid = %s
    ''', [roomid])
    return curs.fetchall()
