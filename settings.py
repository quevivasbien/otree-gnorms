from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=1.50, doc="",
    mturk_hit_settings=dict(
        keywords='bonus, study, decisions',
        title='Decision-making study',
        description='Academic experiment on decision making from Aix-Marseille University,'
                    ' the University of Chicago, and the University of Utah',
        frame_height=500,
        template='global/mturk_template.html',
        minutes_allotted_per_assignment=60,
        expiration_hours=7 * 24,
        qualification_requirements=[
            # Completed at least 100 HITs
            {
                'QualificationTypeId': '00000000000000000040',
                'Comparator': 'GreaterThanOrEqualTo',
                'IntegerValues': [100]
            },
            # Has approval rate >= 95%
            {
                'QualificationTypeId': '000000000000000000L0',
                'Comparator': 'GreaterThanOrEqualTo',
                'IntegerValues': [95]
            },
            # Is adult
            {
                'QualificationTypeId': '00000000000000000060',
                'Comparator': 'EqualTo',
                'IntegerValue': 1
            },
            # Is in US
            {
                'QualificationTypeId': '00000000000000000071',
                'Comparator': 'EqualTo',
                'LocaleValues': [{'Country': 'US'}]
            },
            # Has not already taken survey
            {
                'QualificationTypeId': '3VVYNZTOMVAZHDRJGI7F78SBKS5ADF',
                'Comparator': 'DoesNotExist'
            }
        ],
        grant_qualification_id='3VVYNZTOMVAZHDRJGI7F78SBKS5ADF'  # to prevent retakes
    )
)

SESSION_CONFIGS = [
     # dict(
     #    name='gender_norms',
     #    display_name="Gender norms of self-promotion",
     #    num_demo_participants=50,
     #    app_sequence=['gender_norms']
     # ),
     # dict(
     #    name='gender_norms_v2',
     #    display_name="Gender norms of self-promotion, with extra questions",
     #    num_demo_participants=50,
     #    app_sequence=['gender_norms_v2']
     # ),
     dict(
        name='test',
        display_name='Test to establish performance distribution',
        num_demo_participants=50,
        app_sequence=['test']
         ),
     dict(
        name='applicant',
        display_name="Applicant",
        num_demo_participants=50,
        app_sequence=['applicant']
         ),
     dict(
        name='employer',
        display_name="Employer",
        num_demo_participants=50,
        app_sequence=['employer']
         )
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

EXTENSION_APPS = [
    'captcha',
]

RECAPTCHA_PUBLIC_KEY = '6LdWJsMZAAAAAAeXmwaUt1Whil_vaRJgXZ_Z9lZu'
RECAPTCHA_PRIVATE_KEY = environ.get('RECAPTCHA_PRIVATE_KEY')
