from django.db import connections
from djtinue.admissions.models import LivewhaleEvents
from djtinue.admissions.models import STYPES

from django.utils.timezone import localtime
from django.utils.dateformat import DateFormat

from django.utils.encoding import smart_text, force_text

cursor = connections['livewhale'].cursor()

session_type="undergraduate-studies"

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

print sql

cursor.execute(sql)

# format:
# Thu. May 01, 2014 at 06pm (Master of Education & ACT Info Session)
for event in cursor.fetchall():
    lc = localtime(event[2])
    df = DateFormat(lc)
    day = df.format('D')
    date = df.format('M d, Y')
    time = df.format('h:ia')
    event = force_text(event[1])
    title = "%s. %s at %s (%s)" % (day, date, time , event)

    print title
