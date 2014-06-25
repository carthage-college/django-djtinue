from django import forms
from django.conf import settings

from djtools.fields import STATE_CHOICES, COUNTRIES
from djtools.fields import GENDER_CHOICES, BINARY_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Contact
from djforms.processors.forms import ContactForm

from localflavor.us.forms import USPhoneNumberField, USZipCodeField
from localflavor.us.forms import USSocialSecurityNumberField
from sqlalchemy import create_engine
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger(__name__)

NOW    = datetime.now()
MONTH  = int(NOW.month)
YEAR   = int(NOW.year)
YEAR7  = YEAR
YEAR14 = YEAR
YEARS1 =  [x for x in reversed(xrange(1926,date.today().year +1))]
YEARS3 =  [x for x in reversed(xrange(1926,date.today().year +3))]


EDUCATION_GOAL = (
    (1,"I would like to earn my first bachelor's degree."),
    (5,"""
        I already have a bachelor's degree
        and now would like to earn certification to teach.
    """),
    (7,"I would like to take classes for my own personal interest."),
)

PROGRAM_CHOICES = (
    ("7","7 week format"),
    ("14","14 week Undergraduate or Graduate"),
)

# 7 week years
if MONTH >= 8:
    YEAR7 += 1

# 14 week years
if MONTH > 2 and MONTH <= 10:
    YEAR14 += 1

SESSION7 = (
    ("7-AG-%s" % YEAR7, "January %s" % YEAR7),
    ("7-AK-%s" % YEAR7, "February %s" % YEAR7),
    ("7-AM-%s" % YEAR7, "April %s" % YEAR7),
    ("7-AS-%s" % YEAR7, "May %s" % YEAR7),
    ("7-AT-%s" % YEAR7, "July %s" % YEAR7),
)
if MONTH < 9:
    YEAR7 = YEAR
SESSION14 = (
    ("14-A-%s" % YEAR14, "September %s" % YEAR7),
    ("14-C-%s" % YEAR14, "February %s" % YEAR14),
)

class AdultContactForm(ContactForm):
    """
    Adult Ed contact form based on the generic processor
    contact model & its form
    """
    address1     = forms.CharField(max_length=128, label="School address")
    address2     = forms.CharField(max_length=128, label="", required=False)
    city         = forms.CharField(max_length=128)
    state        = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code  = USZipCodeField(label="Zip Code")

    class Meta:
        model = Contact
        fields = (
            'first_name','second_name','last_name','previous_name',
            'address1','address2','city','state','postal_code','email','phone'
        )

    def __init__(self,*args,**kwargs):
        super(AdultContactForm,self).__init__(*args,**kwargs)
        self.fields['state'].widget.attrs['class'] = 'required'

class PersonalForm(forms.Form):
    """
    personal data
    """
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect()
    )
    ss_num = USSocialSecurityNumberField(
        label = "Social security number"
    )
    dob = forms.DateField(
        label = "Date of birth", help_text="Format: dd/mm/yyyy"
    )
    cob = forms.CharField(
        label = "City of birth",
        max_length=128
    )
    sob = forms.CharField(
        label = "State/Provence of birth",
        max_length=128
    )
    pob = forms.CharField(
        label = "Country of birth",
        max_length=128
    )
    military = forms.TypedChoiceField(
        label="Have you ever served in the military?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )

class EmploymentForm(forms.Form):
    """
    employment history
    """
    # current employment
    employer  = forms.CharField(max_length=128, required=False)
    position = forms.CharField(max_length=128, required=False)
    tuition_reimburse = forms.TypedChoiceField(
        label="Does your employer offer tuition reimbursement?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )

class EducationGoalsForm(forms.Form):

    educationalgoal = forms.TypedChoiceField(
        label="What degree are you intending to pursue?",
        choices=EDUCATION_GOAL, widget=forms.RadioSelect()
    )
    program = forms.TypedChoiceField(
        label="Choose the scheduling format",
        choices=PROGRAM_CHOICES, widget=forms.RadioSelect()
    )
    session7 = forms.TypedChoiceField(
        label="Upcoming 7 Week Sessions", required=False,
        choices=SESSION7, widget=forms.RadioSelect()
    )
    session14 = forms.TypedChoiceField(
        label="Upcoming 14 Week Sessions", required=False,
        choices=SESSION14, widget=forms.RadioSelect()
    )
    intended_major = forms.CharField(max_length=128, required=False)
    intended_minor = forms.CharField(max_length=128, required=False)

    def clean(self):
        if not self.cleaned_data.get('session7') \
          and not self.cleaned_data.get('session14'):
            self._errors["session7"] = self.error_class(
                ["Choose either a 7 or 14 week upcoming session"]
            )
        return self.cleaned_data

class ApplicationFeeForm(forms.Form):
    """
    Application Fee form
    """
    amount = forms.CharField(widget=forms.HiddenInput(), initial="$10.00")
    payment_type = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )

def _insert(data):
    """
    private method to insert data into informix
    for continuing education applications
    """

    DATE = datetime.now().strftime("%m/%d/%Y")
    YEAR = int(datetime.now().strftime("%Y"))
    MONTH = int(datetime.now().strftime("%m"))
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
    logger.debug("create uid sql = %s" % sql)
    connection.execute(sql)

    # get uid
    sql = "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"
    logger.debug("get uid sql = %s" % sql)
    uid = connection.execute(sql)
    apptmp_no = uid.fetchone()[0]
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
    logger.debug("contact info sql = %s" % sql)
    connection.execute(sql)

    # jenzabar freakiness
    sql =   """
            INSERT INTO app_sitetmp_rec
                (id, home, site, beg_date)
            VALUES (%s, "Y", "CART", "%s")
            """ % (apptmp_no, DATE)
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
            add_date, parent_contr, enrstat, rank, emailaddr,
            prog, subprog, upd_uid, add_uid, upd_date, act_choice,
            stuint_wt, jics_candidate
        )
        VALUES (
            %s,"Y", "%s", "%s", "4", "%s", "0.00", "", "0",
            "%s", "%s", "%s", "0", "0", "%s", "", "0", "N"
        ) """ % (
            apptmp_no,start_session,start_year,
            DATE,data["contact"]["email"], program4, subprogram,DATE
        )
    logger.debug("session info sql = %s" % sql)
    connection.execute(sql)

    # personal info
    sql = """
        INSERT INTO app_proftmp_rec (
            id, birth_date, birthplace_city, birthplace_st, birthplace_ctry
            sex, church_id, prof_last_upd_date
        )
        VALUES (
            %s,"%s","%s","%s","0","%s"
        ) """ % (
            apptmp_no,
            data["personal"]["dob"],
            data["personal"]["cob"],
            data["personal"]["sob"],
            data["personal"]["pob"],
            data["personal"]["gender"],DATE
        )
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
    logger.debug("payment info sql = %s" % sql)
    connection.execute(sql)
    connection.close()
