REGIONS = (
    ('AM', 'Amhara'),
    ('TG', 'Tigrai')
)

JOB_STATUS_OPEN   = 1
JOB_STATUS_CLOSE  = 2
JOB_STATUS = (
    (JOB_STATUS_OPEN, 'Opened'),
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
