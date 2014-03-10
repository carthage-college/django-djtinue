from djzbar.utils.informix import do_sql

DEPARTMENTS = """SELECT unique descr, hrdept, hrdiv
FROM hrdept_table
WHERE end_date is null
AND hrdiv not in ("EMER")
AND descr not in ("College Official", "Pending Employee", "Student Worker")
ORDER BY descr"""

objs = do_sql(DEPARTMENTS, key="debug")
print objs

for obj in objs:
    print obj

