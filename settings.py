from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",
    mturk_hit_settings = dict(
        keywords='bonus, study, decisions',
        title='Decision-making study',
        description='Academic experiment on decision making from University of Utah and Aix-Marseille University',
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
            }
            # Is in US
            {
                'QualificationTypeId': '00000000000000000071',
                'Comparator': 'EqualTo',
              	'LocaleValues': [{'Country': 'US'}]
            }
            # Has not already taken survey
            {
                'QualificationTypeId': '303SJT1CWE1SIJV6J0XUXHLQB1Q4F7',
                'Comparator': 'DoesNotExist'
            }
        ]
        grant_qualification_id='303SJT1CWE1SIJV6J0XUXHLQB1Q4F7' # to prevent retakes
        # TODO: Change qualifcation ID to an id controlled by Pavitra's account
    )
)

SESSION_CONFIGS = [
     dict(
        name='prefsranker',
        display_name="Preferences Ranker",
        num_demo_participants=1,
        app_sequence=['prefsranker']
     ),
     dict(
        name='gender_norms',
        display_name="Gender norms of self-promotion",
        num_demo_participants=50,
        app_sequence=['gender_norms']
     ),
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

SECRET_KEY = '2066etnf4@egr9t8yfyg7*5zg+2it3du@k0c82vwh8jri1+_hu'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

EXTENSION_APPS = [
    'captcha',
]

RECAPTCHA_PUBLIC_KEY = '6LcvN7wZAAAAACrkDlIMQl1sMCQhFF1fc8GkV43T'
RECAPTCHA_PRIVATE_KEY = '6LcvN7wZAAAAAHG3R9BRlH_s5dtznelvRYiSMPo8'
