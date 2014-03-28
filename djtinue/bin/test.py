from djzbar.utils.informix import do_sql

DEPARTMENTS = """SELECT unique descr, hrdept, hrdiv
FROM hrdept_table
WHERE end_date is null
AND hrdiv not in ("EMER")
AND descr not in (
    "Officer of the College","Pending Employee","Student Worker",
    "EXSS Department","Bookstore","College Official","China Internship"
)
ORDER BY descr"""

objs = do_sql(DEPARTMENTS, key="debug")

for obj in objs:
    print obj

