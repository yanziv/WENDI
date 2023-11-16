import cs304dbi as dbi

def show_rooms(conn, dormid):
    '''return all rooms with specified dormid as the hid'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select number from room where hid = %s
    ''', [dormid])
    return curs.fetchall()