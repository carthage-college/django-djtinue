from django.conf import settings

from sqlalchemy import create_engine
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger(__name__)

def _insert(data):
    """
    private method to insert data into informix
    for continuing education applications
    """

    DATE = datetime.now().strftime("%m/%d/%Y")
    TIME = datetime.now().strftime("%H%M")
    PURGE_DATE = (
        date.today() + relativedelta( months = +2 )
    ).strftime("%m/%d/%Y")

    engine = create_engine(settings.INFORMIX_EARL)
    connection = engine.connect()

    # create unifying id number (uid)
    sql =   '''
        INSERT INTO
            apptmp_rec (add_date,add_tm,app_source,stat)
        VALUES ("%s","%s","AEA","P")
    ''' % (DATE,TIME)
    if settings.DEBUG:
        logger.debug("create uid sql = %s" % sql)
    connection.execute(sql)

    # get uid
    sql = "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"
    if settings.DEBUG:
        logger.debug("get uid sql = %s" % sql)
    uid = connection.execute(sql)
    apptmp_no = uid.fetchone()[0]
    if settings.DEBUG:
        logger.debug("uid = %s" % apptmp_no)

    # contact information (plus ss_num)
    sql =   """
            INSERT INTO app_idtmp_rec (
                id, firstname, middlename, lastname,
                addr_line1, addr_line2, city, st, zip, ctry,
                phone, ss_no, aa, add_date, ofc_add_by, upd_date, purge_date,
                prsp_no, name_sndx, correct_addr, decsd, valid)
            VALUES
                (%s,"%s","%s","%s","%s","%s","%s","%s","%s","USA",
                "%s","%s","PERM","%s","ADLT","%s","%s","0", "", "Y", "N", "Y")
            """ % (
                apptmp_no,data["contact"]["first_name"],
                data["contact"]["second_name"],data["contact"]["last_name"],
                data["contact"]["address1"],data["contact"]["address2"],
                data["contact"]["city"],data["contact"]["state"],
                data["contact"]["postal_code"],data["contact"]["phone"],
                data["personal"]["ss_num"],DATE,DATE,PURGE_DATE
            )
    if settings.DEBUG:
        logger.debug("contact info sql = %s" % sql)
    connection.execute(sql)

    # jenzabar freakiness
    sql =   """
            INSERT INTO app_sitetmp_rec
                (id, home, site, beg_date)
            VALUES (%s, "Y", "CART", "%s")
            """ % (apptmp_no, DATE)
    if settings.DEBUG:
        logger.debug("jenzabar freakiness sql = %s" % sql)
    connection.execute(sql)

    # Education plans
    #
    # decode programs, subprograms, plan_enr_sess and plan_enr_yr
    if data["education"]["educationalgoal"] in (1,2,5,6,7):
        program4 = "UNDG"
        if data["education"]["program"] == "7":
            subprogram = "7WK"
        else:
            subprogram="PTSM"
    elif data["education"]["educationalgoal"] == "3":
        program4 = "GRAD"
        subprogram="MED"
    elif data["education"]["educationalgoal"] == "4":
        program4 = "ACT"
        subprogram = "ACT"
    else:
        program4 = ""
        subprogram = ""

    # seesion info from code: e.g. 14-C-2014
    if data["education"]["program"] == "7":
        start = data["education"]["session7"].split('-')
    elif data["education"]["program"] == "14":
        start = data["education"]["session14"].split('-')
    if isinstance(start, list):
        plan_enr_sess = start[0]
        plan_enr_yr = start[2]
        start_session = start[0]
        start_year = start[2]
    else:
        plan_enr_sess = ""
        plan_enr_yr = ""
        start_session = ""
        start_year = ""

    sql = """
        INSERT INTO app_admtmp_rec (
            id, primary_app, plan_enr_sess, plan_enr_yr, intend_hrs_enr,
            add_date, parent_contr, enrstat, rank, emailaddr,major
            prog, subprog, upd_uid, add_uid, upd_date, act_choice,
            stuint_wt, jics_candidate
        )
        VALUES (
            %s,"Y", "%s", "%s", "4", "%s", "0.00", "", "0",
            "%s", "%s", "%s", "0", "0", "%s", "", "0", "N"
        ) """ % (
            apptmp_no,start_session,start_year,DATE,
            data["contact"]["email"][:32],data["education"]["intended_major"],
            program4,subprogram,DATE
        )
    if settings.DEBUG:
        logger.debug("session info sql = %s" % sql)
    connection.execute(sql)

    # personal info
    sql = """
        INSERT INTO app_proftmp_rec (
            id, birth_date, birthplace_city, sex, church_id,
            prof_last_upd_date
        )
        VALUES (
            %s,"%s","%s","%s","0","%s"
        ) """ % (
            apptmp_no, data["personal"]["dob"].strftime("%m/%d/%Y"),
            data["personal"]["pob"], data["personal"]["gender"], DATE
        )
    if settings.DEBUG:
        logger.debug("more personal info sql = %s" % sql)
    connection.execute(sql)

    # schools
    for school in data["schools"]:
        code = school.school_code
        if not code:
            code = 0000
        # attended from
        try:
            attend_from = datetime(
                int(school.from_year),int(school.from_month), 1
            ).strftime("%m/%d/%Y")
        except:
            attend_from = datetime(1900,1,1).strftime("%m/%d/%Y")
        # attende to
        try:
            attend_to = datetime(
                int(school.to_year),int(school.to_month), 1
            ).strftime("%m/%d/%Y")
        except:
            attend_to = datetime(1900,1,1).strftime("%m/%d/%Y")
        # grad date
        try:
            grad_date = datetime(
                int(school.grad_year),int(school.grad_month), 1
            ).strftime("%m/%d/%Y")
        except:
            grad_date = datetime(1900,1,1).strftime("%m/%d/%Y")

        sql = """
            INSERT INTO app_edtmp_rec (
                id, ceeb, fullname, city, st, enr_date, dep_date, grad_date,
                stu_id, sch_id, app_reltmp_no, rel_id,priority, zip, aa, ctgry
            )
            VALUES (
                %s,"%s","%s","%s","%s","%s","%s","%s",0,0,0,0,0,"", "ac","COL"
            )
            """ % (
                apptmp_no, code, school.school_name, school.school_city,
                school.school_state, attend_from, attend_to, grad_date
            )
        if settings.DEBUG:
            logger.debug("school info sql = %s" % sql)
        connection.execute(sql)

    # payment info
    sql = """
        UPDATE
            apptmp_rec
        SET
            payment_method = "%s", stat = "H"
        WHERE
            apptmp_no = %s
        """ % (data["fee"]["payment_type"], apptmp_no)
    if settings.DEBUG:
        logger.debug("payment info sql = %s" % sql)
    connection.execute(sql)
    connection.close()
