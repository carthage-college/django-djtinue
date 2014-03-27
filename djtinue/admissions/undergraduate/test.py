from djzbar.settings import INFORMIX_EARL_TEST

from sqlalchemy import create_engine
from datetime import datetime

import sys

def main():

    DATE = datetime.now().strftime("%m-%d-%Y")
    TIME = datetime.now().strftime("%H%M")

    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()

    # create id
    sql = '''
        INSERT INTO apptmp_rec (
            add_date,add_tm,app_source,stat
        )
        VALUES (
            %s, %s, "AEA", "P")
    ''' % (DATE,TIME)

    connection.execute(sql)

    # this sql query returns the same uid as the query after it
    sql = """
        SELECT
            apptmp_no
        FROM
            apptmp_rec
        WHERE
            apptmp_no = DBINFO( 'sqlca.sqlerrd1' )
    """

    # get unifying id (uid)
    sql = "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"

    objects = connection.execute(sql)
    apptmp_no = objects.fetchone()[0]

    print apptmp_no

    connection.close()

if __name__ == "__main__":
    sys.exit(main())

