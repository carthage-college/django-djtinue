#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import connections
from django.utils.dateformat import DateFormat
from django.utils.timezone import localtime


# dictionary name corresponds to URL slug
STYPES = {
    'information-session': 712,
    'graduate-education': 715,
    'undergraduate-studies': 713,
    'master-social-work': 714,
    'paralegal': 582,
}

session_type = 'paralegal'
cursor = connections['livewhale'].cursor()
sql = """
    SELECT
        id, title, date_dt
    FROM
        livewhale_events
    WHERE
        id IN (
            select id2 from livewhale_tags2any where id1={0}
        )
    AND
        id IN (
            select id2 from livewhale_tags2any where id1={1}
        )
    AND
        date_dt > DATE(NOW())
    ORDER BY
        date_dt
""".format(STYPES['information-session'], STYPES[session_type])
cursor.execute(sql)

for event in cursor.fetchall():
    lc = localtime(event[2])
    df = DateFormat(lc)
    day = df.format('D')
    date = df.format('M d, Y')
    time = df.format('h:ia')
    title = '{0}. {1} at {2} ({3})'.format(day, date, time, event[1])
    print(title)
