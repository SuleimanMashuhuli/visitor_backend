__author__ = 'Suleiman Ali Mashuhuli'

ID_TYPES = [
    ('national_id', 'National ID'),
    ('passport', 'Passport'),
    ('pin', 'PIN'),
]

STATUS_CHOICES = [
    ('check_in', 'Check In'),
    ('check_out', 'Check Out'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('declined', 'Declined'),
    ('cancelled', 'Cancelled')
]

TYPE_VISIT = [
    ('internal', 'Internal'),
    ('external_appointment', 'External Appointment'),
    ('external_walkin', 'External Walkin')
]

ROLES_CHOICE = [
    ('admin', 'Admin'),
    ('security', 'Security'),
    ('host', 'Host')
]

