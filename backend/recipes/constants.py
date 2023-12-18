# FOODGRAM SETTINGS AND CONSTANTS

# Set user model field that is used as unique identifier
USERNAME_FIELD_CONST = 'email'

# Set field list that required for creating a user via createsuperuser command
REQUIRED_FIELDS_CONST = ('username', 'password')

# Minimum number for values in django models
MIN_AMOUNT = 1

# Maximum number for values in django models
MAX_AMOUNT = 32767

# Maximum number of symbols for colorfield in django models
MAX_HEX = 7

# Maximum length of symbols for email field in django models
MAX_LEN_EMAIL = 254

# Maximum length of symbols for name field in django models
MAX_LEN_NAME = 150

# Maximum length of symbols for title field in django models
MAX_LEN_TITLE = 200

# Maximum number of extra inline forms to use in Admin site
ADMIN_INLINE_EXTRA = 1