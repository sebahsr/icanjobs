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

MONTHS = {
    ('jan', 'January'),
    ('feb', 'Febraury'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'Septemeber'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December')
}

EDIT_SEC_SKILL = 'skill'
EDIT_SEC_EXPR = 'experience'
EDIT_SEC_EDUC = 'education'
EDIT_SEC_WEBS = 'website'
EDIT_SEC_GENR = 'general'
PAG_JOB_NUMBER = 10
PAG_BLOG_NUMBER = 6
RECENT_JOBS_NUMBER = 5
SEEN_UNSEEN_STATUS = (
    ('read', 'Seen'),
    ('unread', 'Not Seen')
)