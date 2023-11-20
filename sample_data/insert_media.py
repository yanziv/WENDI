'''Populates the picfile table from files in the 'uploads' directory.
'''

import os
import cs304dbi as dbi
    
def insert(conn, url, uid, rid):
    curs = dbi.cursor(conn)
    try:
        curs.execute('''INSERT INTO media (url, uid, rid) 
                        VALUES (%s, %s, %s)''',
                    [url, uid, rid])
        conn.commit()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    db_to_use = 'wendi_db' 
    print('will connect to {}'.format(db_to_use))
    dbi.conf(db_to_use)
    conn = dbi.connect()
    insert(conn, 'media/review/test_1.png', 2, 1)
    insert(conn, 'media/review/test_2.png', 3, 2)
    insert(conn, 'media/review/test_3.png', 1, 3)