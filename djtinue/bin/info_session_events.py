from django.db import connections
from django.utils.timezone import localtime
from django.utils.dateformat import DateFormat

from djtinue.admissions.models import LivewhaleEvents

# dictionary name corresponds to URL slug
STYPES = {
    "information-session":712,
    "graduate-education":715,
    "undergraduate-studies":713,
    "master-social-work":714,
    "paralegal":582
}

session_type="paralegal"
cursor = connections['livewhale'].cursor()
sql = """
            SELECT
                id,title,date_dt
            FROM
                livewhale_events
            WHERE
                id IN (
                    select id2 from livewhale_tags2any where id1=%s
                )
            AND
                id IN (
                    select id2 from livewhale_tags2any where id1=%s
                )
            AND
                date_dt > DATE(NOW())
            ORDER BY
                date_dt
""" % (STYPES["information-session"],STYPES[session_type])
cursor.execute(sql)

for event in cursor.fetchall():
    lc = localtime(event[2])
    df = DateFormat(lc)
    day = df.format('D')
    date = df.format('M d, Y')
    time = df.format('h:ia')
    title = "%s. %s at %s (%s)" % (day, date, time , force_text(event[1]))
    print title

