from django.db import models

class AdultEdModel(models.Model):

    #A bunch of fields below - production table information after field

    student_id = models.PositiveIntegerField(max_length=7) #aa_rec id int
    first_name = models.CharField(max_length=200) #id_rec firstname char(32)
    middle_name = models.CharField(max_length=200, null=True, blank=True) #id_rec middlename char(32)
    last_name = models.CharField(max_length=200) #id_rec lastname char(32)

    CONCENTRATION = (
        ('ACTE', 'ACT Secondary Ed'),
        ('ACTS', 'ACT Special Education'),
        ('ARCH', 'Archaeology'),
        ('CCER', 'Coaching Certification'),
        ('COEC', 'Conservation and Ecology'),
        ('CRWR', 'Creative Writing'),
        ('EVDT', 'Environmental Data'),
        ('EVED', 'Environmental Education'),
        ('EVPO', 'Environmental Policy'),
        ('GIS', 'Geo. Information Sci'),
        ('INED', 'Instrumental Music Edu'),
        ('INPR', 'Instrumental Performance'),
        ('MADM', 'Masters-Administration'),
        ('MCAR', 'Masters-Creative Arts'),
        ('MCCS', 'Special Education'),
        ('MGAT', 'Gifted and Talented'),
        ('MGUC', 'Guidance and Counseling'),
        ('MLAG', 'Language Arts'),
        ('MMLA', 'Modern Language'),
        ('MNAS', 'Natural Science'),
        ('MRED', 'Reading'),
        ('MREL', 'Religion'),
        ('MSCS', 'Constitutional Studies'),
        ('MSOC', 'Social Science'),
        ('MTEL', 'Teacher Leadership'),
        ('MUCH', 'Choral and General'),
        ('MUCM', 'Church Music'),
        ('MUED', 'Musical Education'),
        ('MUIN', 'Instrumental'),
        ('MUJZ', 'Jazz'),
        ('MUPD', 'Piano Pedagogy'),
        ('MUPR', 'Performance'),
        ('MUSI', 'Music'),
        ('MUTH', 'Music Theatre'),
        ('PLAW', 'Criminal Justice Pre-Law'),
        ('PRCM', 'CMA Program'),
        ('PRRB', 'Rosebud Institute'),
        ('PRSL', 'Summer Language Seminars'),
        ('SSEC', 'Social Science Econ'),
        ('SSGE', 'Social Science Geography'),
        ('SSHI', 'Social Science History'),
        ('SSPO', 'Social Science Pol. Sci'),
        ('SSPS', 'Social Science Psych'),
        ('SSSO', 'Social Science Sociology'),
        ('UNDC', 'Undecided'),
        ('VOED', 'Vocal Music Education'),
        ('VOPR', 'Vocal Performance'),
        ('WALF', 'Water and Life'),
    )

    #'concentration' is rendered as a select
    concentration = models.CharField(max_length=200, choices=CONCENTRATION) #acad_rec conc1 char(4), conc2 char(4), conc3 char(4)

    participate_in_ceremony = models.BooleanField() # gradwalk_rec plan2walk char(1)

    FINISHED_CLASSES_IN = (
        ('RA', 'Fall'),
        ('RB', 'JTerm'),
        ('RC', 'Spring'),
        ('RE', 'Summer'),
    )
    finished_classes_in = models.CharField(max_length=200, choices=FINISHED_CLASSES_IN) #gradwalk_rec grad_sess char(4)

    phone_number = models.CharField(max_length=16) #aa_rec phone char(12)
    email = models.EmailField(max_length=100) #aa_rec line1 char(64)
    is_carthage_email = False #Boolean that will be true if the email is a carthage email

    address = models.CharField(max_length=200) #id_rec addr_line1 char(64)
    city = models.CharField(max_length=200) #aa_rec city char(50)
    state = models.CharField(max_length=2) #aa_rec st char(2)
    zip = models.PositiveIntegerField(max_length=5) #aa_rec zip char(10)

    date = models.DateField(auto_now_add=True) #This field doesn't show up, 'auto_now_add' makes it invisible

    #Global options
    class Meta:
        verbose_name = 'Masters Education' #The name of the form as it appears on the admin page
        verbose_name_plural = 'Masters Education' # " " but in a plural form
