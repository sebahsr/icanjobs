REGIONS = (
    ('AM', 'Amhara'),
    ('TG', 'Tigrai')
)

JOB_STATUS_OPEN   = 1
JOB_STATUS_CLOSE  = 2
JOB_STATUS = (
    (JOB_STATUS_OPEN, 'Open'),
    (JOB_STATUS_CLOSE, 'Closed')
)

COUNTRIES = (

    ('ET', "Ethopia"),
    ("ER", "Eritrea")
)
DEFAULT_ERR = 0
DEFAULT_SUC = 1
JOB_ERR_APPLIED_ALREADY = 2
JOB_SUC_APPLIED = 3

feedback_message = {
    DEFAULT_SUC : "Task succesfully complted",
    DEFAULT_ERR : "Cant complete the task. Something went wrong. ",
    JOB_ERR_APPLIED_ALREADY : "You have applied to the job already",
    JOB_SUC_APPLIED : "You have succesfully applied to the job",
}

PAY_PERIOD = {
    ('year', 'Per Year'),
    ('month', 'Per Month'),
    ('day', 'Per Day'),
    ('hour', 'Per Hour'),
}

MONTHS = (
    ('jan', 'January'),
    ('feb', 'February'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'September'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December')
)

EDIT_SEC_SKILL = 'skill'
EDIT_SEC_EXPR = 'experience'
EDIT_SEC_EDUC = 'education'
EDIT_SEC_WEBS = 'website'
EDIT_SEC_GENR = 'general'
EDIT_SEC_CV = 'cv'
EDIT_SEC_LINK = 'worklink'
EDIT_SEC_SAMP = 'worksample'
EDIT_SEC_ASSOC = 'association'
EDIT_SEC_REFER = 'reference'
EDIT_SEC_SUM = 'summary'
EDIT_SEC_VOL = 'volunteer'
PAG_JOB_NUMBER = 20
RECENT_PAG_JOB_NUMBER = 8
PAG_BLOG_NUMBER = 6
RECENT_JOBS_NUMBER = 16
RECENT_BLOG_NUMBER = 3
RECENT_JOBS_SIDEBAR = 4

SEEN_UNSEEN_STATUS = (
    ('read', 'Seen'),
    ('unread', 'Not Seen')
)

GENDER_MALE = 1;
GENDER_FEMALE = 2

EDUCATION_LEVELS = (

    (1, 'TVET'),
    (2, 'Diploma'),
    (3, "Bachelor's Degree"),
    (4, "Graduate/Professional Degree"),
)

EMPLOYEMENT_STATUS = (

    (1, 'Student'),
    (2, 'Fresh graduate'),
    (3, 'Unemployed'),
    (4, 'Employed Part-Time'),
    (5, 'Employed Full-Time')
)

JOB_TYPES = (
    (1, 'Fresh graduate'),
	(2,	'Internship' ),
	(3,	'Volunteer opportunities '),
	(4,	'Junior level positions'),
	(5,	'Senior level positions(management  and leadership )'),
	(6,	'C-level positions'  )
)

JOB_SEEKER_SERVICES = (
	(1, 'Career Coaching'),
	(2,	'Employment Counseling'),
	(3,	'Job Search strategies'),
	(4,	'Interview coaching'),
	(5,	'Resume Assistance/critique'),
	(6,	'Assessment'),
	(7,	'Workshop or Training'),
	(8,	'Job Fair' ),
	(9,	'Industry linkage'  )
)

EMPLOYER_SERVICES = (

	(1,	'Recruitment services /Talent acquisition'),
	(2,	'Head hunting'),
	(3,	'Job Fair' ),
	(4, 'Industry linkage' ),
	(5,	'Workshop or Training'),
	(6,	'Other, please specify' )
)

GENDER_CHOICES = ( ('Male', "Male") , ('Female', "Female") )