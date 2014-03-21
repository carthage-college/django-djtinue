from djzbar.settings import INFORMIX_EARL_TEST
from djzbar.utils.informix import do_sql

from datetime import datetime

import sys

def main():

    DATE = datetime.now().strftime("%m-%d-%Y")
    TIME = datetime.now().strftime("%H%M")

    # create id
    sql =   'INSERT INTO apptmp_rec (add_date,add_tm,app_source,stat) VALUES (%s, %s, "AEA", "P")' % (DATE,TIME)
    do_sql(sql)

    # get unifying id (uid)
    sql =   """
            SELECT apptmp_no
            FROM   apptmp_rec
            WHERE apptmp_no = DBINFO( 'sqlca.sqlerrd1' )
            """
    sql = "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"
    objects = do_sql(sql)

    for r in objects:
        #print(r[0])
        #print(r.cw_no)
        uid = r[0]

    print uid

    connection.close()

if __name__ == "__main__":
    sys.exit(main())

